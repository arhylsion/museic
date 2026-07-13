guide_pages = [
    {
        "en": ("Extend", "Loop and extend audio tracks seamlessly -- automatically detects beat-aligned loop points or lets you set them manually. Perfect for making background music longer. Supports automatic edge-beat sync or manual start/end markers."),
        "id": ("Extend (Perpanjang)", "Memperpanjang audio dengan loop point presisi. Auto-deteksi beat atau atur manual start/end. Cocok untuk membuat musik latar yang lebih panjang tanpa jeda."),
        "jp": ("Extend (延长)", "オーディオをシームレスにループ延长。ビートに合わせたループポイントを自動検出または手動設定可能。BGM制作に最適。"),
    },
    {
        "en": ("Separate", "Isolate vocals and instrumental stems using the Demucs AI engine. Process only a specific time slice to save memory and time. Exports as clean separate files ready for remixing or karaoke."),
        "id": ("Separate (Pisahkan)", "Pisahkan vokal dan instrumental menggunakan AI Demucs. Proses hanya potongan waktu tertentu untuk hemat memori. Ekspor sebagai file terpisah siap pakai."),
        "jp": ("Separate (分離)", "Demucs AIエンジンを使用してボーカルと楽器を分離。特定の時間範囲のみ処理してメモリと時間を節約。"),
    },
    {
        "en": ("Extract", "Automatically detect the most energetic part of a song (the hook or chorus) and extract it. Uses Separate internally to produce clean vocal and instrumental stems of the hook."),
        "id": ("Extract (Ekstrak)", "Deteksi otomatis bagian paling energik dari lagu (hook atau chorus) lalu ekstrak. Menggunakan Separate untuk menghasilkan stem vokal dan instrumental yang bersih."),
        "jp": ("Extract (抽出)", "曲の最も盛り上がる部分（フックまたはサビ）を自動検出して抽出。Separateを使用してクリーンなステムを出力。"),
    },
    {
        "en": ("Mix", "Auto-ducking: lowers background music when voice is detected, raises it back during silence. Features smooth attack and release for natural-sounding transitions. Ideal for podcasts, voiceovers, and live streaming."),
        "id": ("Mix (Campur)", "Auto-ducking: musik latar otomatis mengecil saat ada suara vokal, kembali normal saat hening. Dilengkapi transisi halus (attack/release) untuk hasil natural. Cocok untuk podcast, voiceover, dan live streaming."),
        "jp": ("Mix (ミックス)", "オートダッキング：ボーカル検出時にBGMを下げ、無音時に戻す。スムーズなアタック/リリースで自然なトランジション。ポッドキャストや配信に最適。"),
    },
    {
        "en": ("Optimize", "Normalize audio to broadcast-standard LUFS loudness (default -14 LUFS). Ensures consistent volume levels across platforms like YouTube, Spotify, radio, and podcast directories."),
        "id": ("Optimize (Optimalkan)", "Normalisasi loudness ke standar broadcast (-14 LUFS default). Volume konsisten di YouTube, Spotify, radio, dan direktori podcast."),
        "jp": ("Optimize (最適化)", "放送規格のLUFSラウドネス（デフォルト-14 LUFS）に正規化。YouTube、Spotify、ラジオで一貫した音量を実現。"),
    },
    {
        "en": ("Enhance", "Reduce background noise (hiss, hum, ambient room tone) with adaptive filtering. Boost voice clarity using compressor and EQ. One-click cleanup for vocal recordings and field audio."),
        "id": ("Enhance (Perbaiki)", "Kurangi noise latar (desis, dengung, suara ruangan) dengan filter adaptif. Tingkatkan kejelasan vokal dengan kompresor dan EQ. Pembersihan instan untuk rekaman vokal."),
        "jp": ("Enhance (強化)", "適応フィルターでノイズ（ヒス、ハム、環境音）を低減。コンプレッサーとEQで声を明瞭化。ボーカル録音のワンクリック補正。"),
    },
    {
        "en": ("Trim", "Automatically detect and remove silence and dead air from recordings. Aggressive mode removes shorter pauses for tighter pacing. Perfect for cleaning up podcasts, voice messages, and interviews."),
        "id": ("Trim (Potong)", "Deteksi dan hapus hening dan jeda mati dari rekaman secara otomatis. Mode agresif untuk jeda pendek. Cocok untuk merapikan podcast, pesan suara, dan wawancara."),
        "jp": ("Trim (トリム)", "録音から無音部分を自動検出して削除。アグレッシブモードで短い間隔も除去。ポッドキャストやボイスメッセージの整形に最適。"),
    },
    {
        "en": ("Vibe", "Apply social media audio effects: Slowed (chill, dark atmosphere without reverb), Slowed+Reverb (ethereal with echo ambience), or Nightcore (energetic, pitched up). Ready for TikTok, Reels, and Shorts."),
        "id": ("Vibe (Suasana)", "Efek audio tren media sosial: Slowed (suasana chill/gelap tanpa reverb), Slowed+Reverb (ethereal dengan gema), atau Nightcore (energik, nada tinggi). Siap untuk TikTok, Reels, dan Shorts."),
        "jp": ("Vibe (雰囲気)", "SNS向けオーディオエフェクト：Slowed（落ち着いた雰囲気、リバーブなし）、Slowed+Reverb（幻想的なエコー）、Nightcore（元気な雰囲気）。TikTok、Reels、Shorts対応。"),
    },
]

tips = {
    "en": "Tips\n- Upload any audio file (.mp3, .wav, .ogg, .m4a, .flac)\n- Processed files appear on the right -- click to download\n- All processing runs locally on your device -- nothing leaves your computer",
    "id": "Tips\n- Upload file audio (.mp3, .wav, .ogg, .m4a, .flac)\n- File hasil muncul di kanan -- klik untuk download\n- Semua proses berjalan lokal di perangkat Anda -- tidak ada yang diunggah ke cloud",
    "jp": "Tips\n- オーディオファイル(.mp3, .wav, .ogg, .m4a, .flac)をアップロード\n- 処理結果は右側に表示 -- クリックしてダウンロード\n- すべての処理はローカルデバイス上で実行 -- クラウドに送信されません",
}

total_pages = len(guide_pages)


def render_page(lang, page):
    page = max(1, min(page, total_pages))
    entry = guide_pages[page - 1]
    title, desc = entry[lang]
    return f"### {title}\n\n{desc}"


def render_tips(lang):
    return f"\n\n---\n{tips[lang]}"
