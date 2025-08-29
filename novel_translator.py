import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from googletrans import Translator, LANGUAGES
import threading
import os
import json

class MultiLanguageTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Novel Translator - 小説翻訳者 - 소설 번역기 - 小说翻译器")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')
        
        # Inisialisasi translator
        self.translator = Translator()
        
        # Load terjemahan UI
        self.ui_texts = self.load_ui_translations()
        self.current_lang = "ID"  # Default bahasa Indonesia
        
        # Daftar bahasa yang didukung (kode bahasa: nama bahasa)
        self.supported_langs = {
            "JP": "Japanese",
            "KR": "Korean", 
            "CN": "Chinese (simplified)",
            "EN": "English",
            "ID": "Indonesian"
        }
        
        # Setup UI
        self.setup_ui()
        self.update_ui_language()
        
    def load_ui_translations(self):
        """Load terjemahan untuk teks UI"""
        return {
            "ID": {
                "title": "Alat Penerjemah Novel",
                "subtitle": "Terjemahkan novel atau teks panjang dengan mudah",
                "src_lang": "Bahasa Sumber:",
                "dest_lang": "Bahasa Target:",
                "src_text": "Teks Sumber",
                "dest_text": "Hasil Terjemahan",
                "translate": "Terjemahkan",
                "import": "Impor Teks",
                "export": "Ekspor Hasil",
                "clear": "Bersihkan",
                "ui_lang": "Bahasa Antarmuka:",
                "ready": "Siap",
                "translating": "Sedang menerjemahkan...",
                "part": "Bagian",
                "complete": "Terjemahan selesai",
                "error": "Error terjadi",
                "cleared": "Teks telah dibersihkan",
                "file_loaded": "File dimuat:",
                "file_saved": "File disimpan:",
                "no_text": "Tidak ada teks untuk diterjemahkan!",
                "load_error": "Error memuat file",
                "save_error": "Error menyimpan file"
            },
            "EN": {
                "title": "Novel Translation Tool",
                "subtitle": "Easily translate novels or long texts",
                "src_lang": "Source Language:",
                "dest_lang": "Target Language:",
                "src_text": "Source Text",
                "dest_text": "Translated Result",
                "translate": "Translate",
                "import": "Import Text",
                "export": "Export Result",
                "clear": "Clear",
                "ui_lang": "UI Language:",
                "ready": "Ready",
                "translating": "Translating...",
                "part": "Part",
                "complete": "Translation complete",
                "error": "Error occurred",
                "cleared": "Text cleared",
                "file_loaded": "File loaded:",
                "file_saved": "File saved:",
                "no_text": "No text to translate!",
                "load_error": "Error loading file",
                "save_error": "Error saving file"
            },
            "JP": {
                "title": "小説翻訳ツール",
                "subtitle": "小説や長文を簡単に翻訳",
                "src_lang": "元の言語:",
                "dest_lang": "目標言語:",
                "src_text": "元のテキスト",
                "dest_text": "翻訳結果",
                "translate": "翻訳",
                "import": "テキストをインポート",
                "export": "結果をエクスポート",
                "clear": "クリア",
                "ui_lang": "UIの言語:",
                "ready": "準備完了",
                "translating": "翻訳中...",
                "part": "部分",
                "complete": "翻訳完了",
                "error": "エラーが発生しました",
                "cleared": "テキストをクリアしました",
                "file_loaded": "ファイルを読み込み:",
                "file_saved": "ファイルを保存:",
                "no_text": "翻訳するテキストがありません!",
                "load_error": "ファイルの読み込みエラー",
                "save_error": "ファイルの保存エラー"
            },
            "KR": {
                "title": "소설 번역 도구",
                "subtitle": "소설이나 긴 글을 쉽게 번역",
                "src_lang": "원본 언어:",
                "dest_lang": "목표 언어:",
                "src_text": "원본 텍스트",
                "dest_text": "번역 결과",
                "translate": "번역",
                "import": "텍스트 가져오기",
                "export": "결과 내보내기",
                "clear": "지우기",
                "ui_lang": "UI 언어:",
                "ready": "준비 완료",
                "translating": "번역 중...",
                "part": "부분",
                "complete": "번역 완료",
                "error": "오류 발생",
                "cleared": "텍스트 지움",
                "file_loaded": "파일 불러옴:",
                "file_saved": "파일 저장:",
                "no_text": "번역할 텍스트가 없습니다!",
                "load_error": "파일 불러오기 오류",
                "save_error": "파일 저장 오류"
            },
            "CN": {
                "title": "小说翻译工具",
                "subtitle": "轻松翻译小说或长文本",
                "src_lang": "源语言:",
                "dest_lang": "目标语言:",
                "src_text": "源文本",
                "dest_text": "翻译结果",
                "translate": "翻译",
                "import": "导入文本",
                "export": "导出结果",
                "clear": "清除",
                "ui_lang": "界面语言:",
                "ready": "准备就绪",
                "translating": "翻译中...",
                "part": "部分",
                "complete": "翻译完成",
                "error": "发生错误",
                "cleared": "文本已清除",
                "file_loaded": "文件已加载:",
                "file_saved": "文件已保存:",
                "no_text": "没有要翻译的文本!",
                "load_error": "加载文件错误",
                "save_error": "保存文件错误"
            }
        }
    
    def get_ui_text(self, key):
        """Ambil teks UI berdasarkan kunci dan bahasa saat ini"""
        return self.ui_texts[self.current_lang].get(key, key)
        
    def setup_ui(self):
        # Style configuration
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Header
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        header_frame.columnconfigure(0, weight=1)
        
        self.title_label = ttk.Label(header_frame, style='Header.TLabel')
        self.title_label.grid(row=0, column=0)
        
        self.subtitle_label = ttk.Label(header_frame)
        self.subtitle_label.grid(row=1, column=0, pady=5)
        
        # Main content frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(3, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # UI Language selection
        ttk.Label(main_frame, text=self.get_ui_text("ui_lang")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ui_lang_var = tk.StringVar(value=self.current_lang)
        ui_lang_combo = ttk.Combobox(main_frame, textvariable=self.ui_lang_var, 
                                    values=list(self.supported_langs.keys()), width=5, state="readonly")
        ui_lang_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        ui_lang_combo.bind('<<ComboboxSelected>>', self.change_ui_language)
        
        # Source language selection
        ttk.Label(main_frame, text=self.get_ui_text("src_lang")).grid(row=0, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        self.src_lang = ttk.Combobox(main_frame, values=list(self.supported_langs.values()), width=20, state="readonly")
        self.src_lang.grid(row=0, column=3, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.src_lang.set('English')
        
        # Target language selection
        ttk.Label(main_frame, text=self.get_ui_text("dest_lang")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dest_lang = ttk.Combobox(main_frame, values=list(self.supported_langs.values()), width=20, state="readonly")
        self.dest_lang.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.dest_lang.set('Indonesian')
        
        # Input text area
        input_frame = ttk.LabelFrame(main_frame, padding="5")
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, width=40, height=20, wrap=tk.WORD, font=('Arial', 10))
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Output text area
        output_frame = ttk.LabelFrame(main_frame, padding="5")
        output_frame.grid(row=2, column=2, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, width=40, height=20, wrap=tk.WORD, font=('Arial', 10), state='disabled')
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        # Buttons
        self.translate_btn = ttk.Button(button_frame, command=self.start_translation)
        self.translate_btn.pack(side=tk.LEFT, padx=5)
        
        self.import_btn = ttk.Button(button_frame, command=self.import_text)
        self.import_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = ttk.Button(button_frame, command=self.export_text)
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, command=self.clear_text)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set(self.get_ui_text("ready"))
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
    def update_ui_language(self):
        """Update semua teks UI berdasarkan bahasa yang dipilih"""
        # Update judul dan subtitle
        self.title_label.config(text=self.get_ui_text("title"))
        self.subtitle_label.config(text=self.get_ui_text("subtitle"))
        
        # Update label frame
        for frame in self.root.winfo_children():
            if isinstance(frame, ttk.LabelFrame):
                if "src_text" in frame.winfo_name():
                    frame.config(text=self.get_ui_text("src_text"))
                elif "dest_text" in frame.winfo_name():
                    frame.config(text=self.get_ui_text("dest_text"))
        
        # Update tombol
        self.translate_btn.config(text=self.get_ui_text("translate"))
        self.import_btn.config(text=self.get_ui_text("import"))
        self.export_btn.config(text=self.get_ui_text("export"))
        self.clear_btn.config(text=self.get_ui_text("clear"))
        
        # Update status
        if self.status_var.get() in [self.get_ui_text("ready"), "Siap", "Ready", "準備完了", "준비 완료", "准备就绪"]:
            self.status_var.set(self.get_ui_text("ready"))
        
    def change_ui_language(self, event=None):
        """Ganti bahasa antarmuka"""
        self.current_lang = self.ui_lang_var.get()
        self.update_ui_language()
        
    def get_lang_code(self, lang_name):
        """Dapatkan kode bahasa dari nama bahasa"""
        lang_map = {
            "Japanese": "ja",
            "Korean": "ko",
            "Chinese (simplified)": "zh-cn",
            "English": "en",
            "Indonesian": "id"
        }
        return lang_map.get(lang_name, 'en')
    
    def start_translation(self):
        # Memulai terjemahan di thread terpisah agar GUI tidak freeze
        thread = threading.Thread(target=self.translate_text)
        thread.daemon = True
        thread.start()
    
    def translate_text(self):
        # Mendapatkan teks dari input
        text_to_translate = self.input_text.get("1.0", tk.END).strip()
        
        if not text_to_translate:
            messagebox.showwarning(self.get_ui_text("no_text"), self.get_ui_text("no_text"))
            return
        
        # Mendapatkan kode bahasa
        src_code = self.get_lang_code(self.src_lang.get())
        dest_code = self.get_lang_code(self.dest_lang.get())
        
        # Menonaktifkan tombol dan memulai progress bar
        self.translate_btn.config(state='disabled')
        self.progress.start()
        self.status_var.set(self.get_ui_text("translating"))
        
        try:
            # Menerjemahkan teks (dibagi menjadi bagian-bagian kecil untuk teks panjang)
            chunks = self.split_text(text_to_translate, 1500)  # 1500 karakter per chunk
            translated_text = ""
            
            for i, chunk in enumerate(chunks):
                self.status_var.set(f"{self.get_ui_text('translating')} {self.get_ui_text('part')} {i+1}/{len(chunks)}")
                translated_chunk = self.translator.translate(chunk, src=src_code, dest=dest_code)
                translated_text += translated_chunk.text + " "
            
            # Menampilkan hasil di output text
            self.output_text.config(state='normal')
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated_text)
            self.output_text.config(state='disabled')
            
            self.status_var.set(self.get_ui_text("complete"))
            
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
            self.status_var.set(self.get_ui_text("error"))
        
        # Mengaktifkan kembali tombol dan menghentikan progress bar
        self.translate_btn.config(state='normal')
        self.progress.stop()
    
    def split_text(self, text, max_length):
        """Membagi teks menjadi beberapa bagian dengan panjang maksimum"""
        if len(text) <= max_length:
            return [text]
            
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + max_length
            if end < len(text):
                while end > start and text[end] not in (' ', '.', '!', '?', '\n', '。', '！', '？', '」', '」', '》', '」'):
                    end -= 1
                if end == start:
                    end = start + max_length
            else:
                end = len(text)
            
            chunks.append(text[start:end])
            start = end
        
        return chunks
    
    def import_text(self):
        # Membuka dialog untuk memilih file
        file_path = filedialog.askopenfilename(
            title="Pilih file teks",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert(tk.END, content)
                self.status_var.set(f"{self.get_ui_text('file_loaded')} {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membaca file: {str(e)}")
                self.status_var.set(self.get_ui_text("load_error"))
    
    def export_text(self):
        # Membuka dialog untuk menyimpan file
        file_path = filedialog.asksaveasfilename(
            title="Simpan hasil terjemahan",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                self.output_text.config(state='normal')
                content = self.output_text.get("1.0", tk.END)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.output_text.config(state='disabled')
                messagebox.showinfo("Sukses", "File berhasil disimpan!")
                self.status_var.set(f"{self.get_ui_text('file_saved')} {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan file: {str(e)}")
                self.status_var.set(self.get_ui_text("save_error"))
    
    def clear_text(self):
        # Membersihkan kedua text area
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state='disabled')
        self.status_var.set(self.get_ui_text("cleared"))

def main():
    root = tk.Tk()
    app = MultiLanguageTranslator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
