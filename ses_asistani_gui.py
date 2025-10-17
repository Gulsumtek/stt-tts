import os
import sys
import torch
import sounddevice as sd
import soundfile as sf
import numpy as np
from pathlib import Path
import time
import warnings
import gradio as gr

# Gereksiz uyarıları gizle
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# TTS - Coqui
try:
    from TTS.api import TTS
    COQUI_AVAILABLE = True
except ImportError:
    COQUI_AVAILABLE = False

# STT - Whisper
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

class VoiceAssistantGUI:
    def __init__(self):
        # Dizinler
        self.temp_dir = Path("temp_audio")
        self.clone_dir = Path("voice_clones")
        self.temp_dir.mkdir(exist_ok=True)
        self.clone_dir.mkdir(exist_ok=True)
        
        # Motorlar
        self.tts_engine = None
        self.whisper_model = None
        self.cloned_voice_path = None
        self.current_language = "tr"
        
        # Başlat
        self._initialize()
    
    def _initialize(self):
        """Sistemleri başlat"""
        # TTS
        if COQUI_AVAILABLE:
            try:
                os.environ["COQUI_TOS_AGREED"] = "1"
                self.tts_engine = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
                if torch.cuda.is_available():
                    self.tts_engine.to("cuda")
            except Exception as e:
                print(f"TTS hatası: {e}")
        
        # STT
        if WHISPER_AVAILABLE:
            try:
                self.whisper_model = whisper.load_model("base")
            except Exception as e:
                print(f"Whisper hatası: {e}")
    
    def text_to_speech(self, text, language, use_clone):
        """Text-to-Speech fonksiyonu"""
        if not self.tts_engine:
            return None, "❌ TTS motoru hazır değil!"
        
        if not text.strip():
            return None, "⚠️ Lütfen metin girin!"
        
        try:
            temp_file = self.temp_dir / f"speech_{int(time.time())}.wav"
            
            # Dil kodu
            lang_code = "tr" if language == "Türkçe" else "en"
            
            # Ses klonlama kontrolü
            if use_clone and self.cloned_voice_path and self.cloned_voice_path.exists():
                self.tts_engine.tts_to_file(
                    text=text,
                    file_path=str(temp_file),
                    speaker_wav=str(self.cloned_voice_path),
                    language=lang_code
                )
                message = f"✅ Metin okundu (Klonlanmış ses - {language})"
            else:
                # Varsayılan ses
                speakers = self.tts_engine.speakers if hasattr(self.tts_engine, 'speakers') else None
                if speakers and len(speakers) > 0:
                    self.tts_engine.tts_to_file(
                        text=text,
                        file_path=str(temp_file),
                        speaker=speakers[0],
                        language=lang_code
                    )
                else:
                    self.tts_engine.tts_to_file(
                        text=text,
                        file_path=str(temp_file),
                        language=lang_code
                    )
                message = f"✅ Metin okundu (Varsayılan ses - {language})"
            
            return str(temp_file), message
            
        except Exception as e:
            return None, f"❌ Hata: {str(e)}"
    
    def speech_to_text(self, audio_file, language):
        """Speech-to-Text fonksiyonu"""
        if not self.whisper_model:
            return "❌ Whisper hazır değil!"
        
        if audio_file is None:
            return "⚠️ Lütfen mikrofona konuşun!"
        
        try:
            lang_code = "tr" if language == "Türkçe" else "en"
            
            result = self.whisper_model.transcribe(
                audio_file,
                language=lang_code,
                fp16=False
            )
            
            text = result["text"].strip()
            
            if text:
                return f"📝 Algılanan Metin ({language}):\n\n{text}"
            else:
                return "❌ Konuşma anlaşılamadı."
            
        except Exception as e:
            return f"❌ Hata: {str(e)}"
    
    def full_cycle(self, audio_file, language):
        """Konuş > Metne Çevir > Oku (Tam döngü)"""
        if not self.whisper_model or not self.tts_engine:
            return None, "❌ Motorlar hazır değil!"
        
        if audio_file is None:
            return None, "⚠️ Lütfen mikrofona konuşun!"
        
        try:
            # STT
            lang_code = "tr" if language == "Türkçe" else "en"
            result = self.whisper_model.transcribe(audio_file, language=lang_code, fp16=False)
            text = result["text"].strip()
            
            if not text:
                return None, "❌ Konuşma anlaşılamadı."
            
            # TTS
            temp_file = self.temp_dir / f"cycle_{int(time.time())}.wav"
            
            if self.cloned_voice_path and self.cloned_voice_path.exists():
                self.tts_engine.tts_to_file(
                    text=text,
                    file_path=str(temp_file),
                    speaker_wav=str(self.cloned_voice_path),
                    language=lang_code
                )
            else:
                speakers = self.tts_engine.speakers if hasattr(self.tts_engine, 'speakers') else None
                if speakers and len(speakers) > 0:
                    self.tts_engine.tts_to_file(
                        text=text,
                        file_path=str(temp_file),
                        speaker=speakers[0],
                        language=lang_code
                    )
                else:
                    self.tts_engine.tts_to_file(
                        text=text,
                        file_path=str(temp_file),
                        language=lang_code
                    )
            
            return str(temp_file), f"✅ Algılanan: {text}"
            
        except Exception as e:
            return None, f"❌ Hata: {str(e)}"
    
    def clone_voice(self, audio_file):
        """Ses klonlama"""
        if audio_file is None:
            return "⚠️ Lütfen ses dosyası yükleyin veya kayıt yapın!"
        
        try:
            # Ses dosyasını klonlama dizinine kopyala
            clone_file = self.clone_dir / f"clone_{int(time.time())}.wav"
            
            # Ses dosyasını oku ve kaydet
            data, samplerate = sf.read(audio_file)
            sf.write(str(clone_file), data, samplerate)
            
            self.cloned_voice_path = clone_file
            
            return f"✅ Ses klonlandı!\n📁 Dosya: {clone_file.name}\n\n💡 Artık TTS'de 'Klonlanmış Sesi Kullan' seçeneğini işaretleyin."
            
        except Exception as e:
            return f"❌ Hata: {str(e)}"
    
    def reset_voice(self):
        """Varsayılan sese dön"""
        self.cloned_voice_path = None
        return "✅ Varsayılan sese dönüldü!"


def create_interface():
    """Gradio arayüzünü oluştur"""
    assistant = VoiceAssistantGUI()
    
    # Tema
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="cyan",
    )
    
    with gr.Blocks(theme=theme, title="🎙️ Profesyonel Ses Asistanı") as app:
        gr.Markdown(
            """
            # 🎙️ Profesyonel Ses Asistanı
            ### Coqui TTS + OpenAI Whisper
            **Text-to-Speech • Speech-to-Text • Ses Klonlama**
            """
        )
        
        with gr.Tabs():
            # TAB 1: Text-to-Speech
            with gr.Tab("💬 Text-to-Speech"):
                gr.Markdown("### Metni Sesli Okut")
                
                with gr.Row():
                    with gr.Column():
                        tts_text = gr.Textbox(
                            label="📝 Metin",
                            placeholder="Okutmak istediğiniz metni buraya yazın...",
                            lines=5
                        )
                        tts_lang = gr.Radio(
                            ["Türkçe", "English"],
                            label="🌍 Dil",
                            value="Türkçe"
                        )
                        tts_use_clone = gr.Checkbox(
                            label="🎭 Klonlanmış Sesi Kullan",
                            value=False
                        )
                        tts_btn = gr.Button("🔊 Oku", variant="primary", size="lg")
                    
                    with gr.Column():
                        tts_audio_out = gr.Audio(label="🎵 Ses Çıktısı", type="filepath")
                        tts_status = gr.Textbox(label="📊 Durum", lines=2)
                
                tts_btn.click(
                    fn=assistant.text_to_speech,
                    inputs=[tts_text, tts_lang, tts_use_clone],
                    outputs=[tts_audio_out, tts_status]
                )
            
            # TAB 2: Speech-to-Text
            with gr.Tab("🎤 Speech-to-Text"):
                gr.Markdown("### Konuşmayı Metne Çevir")
                
                with gr.Row():
                    with gr.Column():
                        stt_audio = gr.Audio(
                            label="🎤 Mikrofon veya Ses Dosyası",
                            type="filepath",
                            sources=["microphone", "upload"]
                        )
                        stt_lang = gr.Radio(
                            ["Türkçe", "English"],
                            label="🌍 Dil",
                            value="Türkçe"
                        )
                        stt_btn = gr.Button("📝 Metne Çevir", variant="primary", size="lg")
                    
                    with gr.Column():
                        stt_text_out = gr.Textbox(
                            label="📄 Çevrilmiş Metin",
                            lines=10
                        )
                
                stt_btn.click(
                    fn=assistant.speech_to_text,
                    inputs=[stt_audio, stt_lang],
                    outputs=stt_text_out
                )
            
            # TAB 3: Tam Döngü
            with gr.Tab("🔄 Tam Döngü"):
                gr.Markdown("### Konuş → Metne Çevir → Oku")
                
                with gr.Row():
                    with gr.Column():
                        cycle_audio = gr.Audio(
                            label="🎤 Mikrofon",
                            type="filepath",
                            sources=["microphone"]
                        )
                        cycle_lang = gr.Radio(
                            ["Türkçe", "English"],
                            label="🌍 Dil",
                            value="Türkçe"
                        )
                        cycle_btn = gr.Button("🔄 Döngüyü Başlat", variant="primary", size="lg")
                    
                    with gr.Column():
                        cycle_audio_out = gr.Audio(label="🎵 Okunan Ses")
                        cycle_status = gr.Textbox(label="📊 Durum", lines=3)
                
                cycle_btn.click(
                    fn=assistant.full_cycle,
                    inputs=[cycle_audio, cycle_lang],
                    outputs=[cycle_audio_out, cycle_status]
                )
            
            # TAB 4: Ses Klonlama
            with gr.Tab("🎭 Ses Klonlama"):
                gr.Markdown(
                    """
                    ### Kendi Sesini Kullan
                    5-10 saniyelik net bir konuşma kaydı yapın veya yükleyin.
                    """
                )
                
                with gr.Row():
                    with gr.Column():
                        clone_audio = gr.Audio(
                            label="🎤 Ses Kaydı (5-10 saniye)",
                            type="filepath",
                            sources=["microphone", "upload"]
                        )
                        with gr.Row():
                            clone_btn = gr.Button("🎭 Sesi Klonla", variant="primary")
                            reset_btn = gr.Button("🔙 Varsayılana Dön", variant="secondary")
                    
                    with gr.Column():
                        clone_status = gr.Textbox(label="📊 Durum", lines=5)
                
                clone_btn.click(
                    fn=assistant.clone_voice,
                    inputs=clone_audio,
                    outputs=clone_status
                )
                
                reset_btn.click(
                    fn=assistant.reset_voice,
                    outputs=clone_status
                )
        
        gr.Markdown(
            """
            ---
            💡 **İpuçları:**
            - Ses klonlama için net ve doğal konuşun
            - TTS'de klonlanmış sesi kullanmak için önce ses klonlayın
            - Tam döngü özelliği konuşmanızı algılayıp size geri okur
            """
        )
    
    return app


if __name__ == "__main__":
    print("\n🚀 Ses Asistanı Arayüzü Başlatılıyor...\n")
    
    if not COQUI_AVAILABLE or not WHISPER_AVAILABLE:
        print("❌ Gerekli kütüphaneler yüklü değil!")
        print("Kurulum: pip install coqui-tts openai-whisper gradio")
        sys.exit(1)
    
    app = create_interface()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )