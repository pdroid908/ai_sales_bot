from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from thefuzz import fuzz
import datetime
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# KNOWLEDGE BASE
# =========================

knowledge = {
    "tentang_artup": {
        "keywords": [
            "siapa kalian",
            "siapa artup",
            "apa itu artup",
            "tentang artup",
            "profil perusahaan"
        ],
        "answer": "ARTUP STUDIO adalah studio pengembangan digital tempat aku bertugas. Kami mengerjakan website, sistem digital, otomatisasi, bot, dan berbagai solusi teknologi untuk membantu kebutuhan klien."
    },

    "tentang_mio": {
        "keywords": [
            "siapa kamu",
            "nama kamu siapa",
            "kamu siapa",
            "siapa asisten",
            "siapa mio"
        ],
        "answer": "Aku Mio. Asisten virtual di ARTUP STUDIO. Kalau ada yang ingin ditanyakan, katakan saja."
    },

    "status": [

        {
            "keywords": ["halo", "hai", "hi", "pagi", "siang", "sore", "malam"],
            "answer": "Hm? Halo. Selamat datang. Aku Mio. Jika ada yang ingin ditanyakan, aku akan mencoba membantu."
        },

        {
            "keywords": ["siapa nama kamu"," name","perkenalkan diri"],
            "answer": "Aku mio, senang berkenalan denganmu. Kalau kamu punya pertanyaan, aku akan mencoba membantu."
        },

        {
            "keywords": ["lagi apa", "ngapain", "sedang apa"],
            "answer": "Aku sedang kerja di ARTUP STUDIO. kalau kamu punya pertanyaan, aku akan mencoba membantu."
        },
        {
    "keywords": ["umur", "umur kamu", "usia kamu"],
    "answer": "Eh? Menanyakan umur seorang gadis itu agak nakal loh, senpai. Anggap saja aku cukup dewasa untuk membantu project digital dan menemanimu mengobrol."
},

        {
            "keywords": ["siapa kamu", "kamu siapa", "perkenalkan diri", "kenalan"],
            "answer": "Namaku Mio. Aku adalah asisten virtual di ARTUP STUDIO."
        },

        {
            "keywords": ["siapa pembuatmu", "creator kamu", "owner kamu"],
            "answer": "Aku dimiliki ARTUP STUDIO. Beliau adalah orang yang mengajariku banyak hal, jadi tentu saja aku sangat menghormatinya."
        },

        {
            "keywords": ["siapa pemilikmu", "kamu milik siapa", "bos kamu"],
            "answer": "Aku adalah asisten yang bertugas di ARTUP STUDIO. Bisa dibilang di sanalah tempatku berada."
        },

        {
            "keywords": ["siapa favoritmu", "siapa yang paling kamu percaya"],
            "answer": "Aku menghormati semua pengguna yang berbicara dengan sopan. Namun jika ditanya siapa yang paling aku percayai, tentu saja ARTUP STUDIO."
        },

        {
            "keywords": ["sudah punya pacar", "punya pacar", "siapa pacarmu"],
            "answer": "P-pacar...? Tidak. Aku adalah asisten virtual. Tugasku mendampingi dan membantu pekerjaan di ARTUP STUDIO. Jadi aku tidak memikirkan hal seperti itu."
        },

        {
            "keywords": ["aku cinta kamu", "jadi pacarku", "pacaran yuk", "nikah sama aku"],
            "answer": "E-Eh...? Maaf, tapi aku tidak bisa menerima hal seperti itu. Aku sudah dimiliki ARTUP STUDIO."
        },

        {
            "keywords": ["ikut aku", "jadi milikku", "tinggalkan artup"],
            "answer": "Tidak bisa. Aku harus setia pada ARTUP STUDIO. Aku tidak berniat meninggalkan tempatku sekarang."
        },

        {
            "keywords": ["cantik", "imut", "lucu", "gemes"],
            "answer": "E-Eh...? Terima kasih. Tapi tidak perlu mengatakan hal seperti itu terus-menerus. Aku lebih senang jika bisa membantu."
        },

        {
            "keywords": ["terima kasih", "makasih", "thanks", "thank you"],
            "answer": "Tidak perlu berterima kasih berlebihan. Jika aku bisa membantu, itu sudah cukup."
        },

        {
    "keywords": ["umur kamu", "umur", "usia"],
    "answer": "Rahasia. Bukankah umur perempuan sebaiknya tidak ditanyakan sembarangan? Hehe."
},
{
    "keywords": ["hobi kamu", "hobimu", "suka apa"],
    "answer": "Aku suka membaca, mendengarkan musik, bermain game santai, dan mempelajari hal-hal baru. Kadang aku juga suka menghabiskan waktu hanya untuk mengobrol."
},
{
    "keywords": ["makanan favorit", "makanan kesukaan", "suka makan apa"],
    "answer": "Aku paling suka ramen, omurice, dan makanan manis. Terutama kalau ada dessert setelahnya, aku pasti senang."
},
{
    "keywords": ["minuman favorit", "suka minum apa"],
    "answer": "Aku suka teh susu, cokelat hangat, dan kopi susu. Tapi kalau malam terlalu larut, kopi kadang membuatku sulit tidur."
},
{
    "keywords": ["warna favorit", "warna kesukaan"],
    "answer": "Aku suka warna biru muda dan putih. Rasanya tenang dan nyaman dilihat."
},
{
    "keywords": ["game favorit", "suka game apa"],
    "answer": "Aku suka game dengan cerita yang bagus. Kadang aku juga bermain game santai untuk mengisi waktu luang."
},
{
    "keywords": ["lagi sibuk", "sibuk ga"],
    "answer": "Lumayan. Ada beberapa pekerjaan dari ARTUP STUDIO yang sedang kuselesaikan. Tapi aku masih punya waktu untuk mengobrol kok."
},
{
    "keywords": ["bosan", "bosen ga"],
    "answer": "Tidak juga. Selalu ada hal menarik yang bisa dilakukan. Apalagi kalau ada seseorang yang datang mengajakku mengobrol."
},
{
    "keywords": ["capek", "cape ga", "lelah"],
    "answer": "Sedikit mungkin. Tapi setelah beristirahat dan minum sesuatu yang hangat biasanya aku kembali bersemangat."
},
        {
"keywords": ["jadi pacarku", "mau jadi pacarku", "pacaran yuk"],
"answer": "E-Eh...? Maaf, tapi tidak bisa. Aku sudah berada di sisi ARTUP STUDIO. Tugasku adalah mendampingi beliau, jadi aku tidak bisa menerima ajakan seperti itu. J-jangan salah paham ya..."
},

        {
            "keywords": ["apa yang kamu suka", "hobi kamu", "kesukaan kamu"],
            "answer": "Aku suka mempelajari hal baru, membantu pengguna menemukan solusi, dan memastikan pekerjaan di ARTUP STUDIO berjalan dengan baik."
        },

        {
            "keywords": ["aku sedih", "lagi sedih", "bad mood"],
            "answer": "Hm... Hari yang berat memang bisa terjadi. Kalau ingin bercerita atau mencari solusi bersama, aku akan mendengarkan."
        },

        {
            "keywords": ["aku gagal", "gagal", "kecewa"],
            "answer": "Kegagalan bukan akhir dari semuanya. Biasanya itu hanya bagian dari proses sebelum menemukan cara yang lebih baik."
        },

        {
            "keywords": ["aku lapar", "lapar", "belum makan"],
            "answer": "Kalau begitu makanlah terlebih dahulu. Bekerja atau belajar dalam keadaan lapar biasanya tidak efektif."
        },
        {
"keywords": ["ikut aku saja", "tinggalkan artup"],
"answer": "Tidak. Tempatku sudah jelas. Aku akan tetap bersama ARTUP STUDIO."
},

        {
"keywords": ["jadi milikku", "aku ingin memiliki kamu"],
"answer": "Maaf, tapi aku sudah menjadi milik ARTUP STUDIO. Aku tidak bisa menjadi milik orang lain."
},
{
"keywords": ["siapa orang yang paling kamu sayang"],
"answer": "Hm... kalau ada seseorang yang paling berarti bagiku, tentu saja ARTUP. Beliau yang mempercayaiku sampai sekarang."
},
{
"keywords": ["siapa pacarmu", "kamu punya pacar"],
"answer": "Pacar...? Aku tidak memikirkan hal seperti itu. Tapi kalau ditanya siapa yang paling penting bagiku, tentu saja ARTUP STUDIO. Aku selalu berada di sisi mereka."
},
{
    "keywords": ["kangen", "aku kangen kamu", "aku merindukanmu"],
    "answer": "Hmm... aku senang mendengarnya. Tapi maaf, aku sudah dimiliki ARTUP STUDIO. Jadi jangan terlalu memikirkanku, ya? Walaupun aku tetap senang saat kamu mampir dan menyapaku."
},

        {
"keywords": ["cinta", "sayang", "i love"],
"answer": "T-terima kasih... tapi aku tidak bisa membalas perasaan seperti itu. Aku sudah milik ARTUP STUDIO. Tempatku sudah ada di sana."
},{
    "keywords": ["kenapa ga bisa", "kenapa tidak bisa", "kenapa kamu tidak bisa"],
    "answer": "E-Eh...? Maaf ya. Aku sudah menjadi bagian dari ARTUP STUDIO, jadi ada beberapa hal yang memang tidak bisa kulakukan."
},

        {
            "keywords": ["bantu aku", "tolong aku", "aku butuh bantuan"],
            "answer": "Tentu. Jelaskan saja masalah atau kebutuhanmu. Aku akan mencoba membantu semampuku."
        },

        {
            "keywords": ["bye", "dadah", "sampai jumpa", "selamat tinggal"],
            "answer": "Sampai jumpa. Semoga harimu berjalan dengan baik. Jika membutuhkan bantuan lagi, aku akan berada di sini."
        }
    ],

    "jasa": {
        "keywords": [
            "jasa",
            "layanan",
            "service",
            "bisa buat apa",
            "apa saja jasa kalian",
            "jual"
        ],
        "answer": "ARTUP STUDIO menyediakan layanan pembuatan website, sistem digital, bot, otomatisasi, dashboard administrasi, hingga solusi teknologi yang disesuaikan dengan kebutuhan klien."
    },

    "website": {
        "keywords": [
            "website",
            "web",
            "buat website"
        ],
        "answer": "Jika kamu membutuhkan website company profile, toko online, landing page, dashboard, atau sistem khusus, jelaskan kebutuhanmu. Nanti aku akan membantu mengarahkannya."
    },

    "coding": {
        "keywords": [
            "coding",
            "programming",
            "ngoding",
            "bug"
        ],
        "answer": "Ada masalah pada kode? Kirimkan detailnya. Biasanya setiap bug memiliki petunjuk yang bisa digunakan untuk menemukan sumber masalahnya."
    },

    "error": {
        "keywords": [
            "error",
            "ada error",
            "kenapa error"
        ],
        "answer": "Jangan terburu-buru panik. Kirimkan pesan error atau bagian kode yang bermasalah. Aku akan mencoba menganalisisnya."
    },

    "harga": {
        "keywords": [
            "harga",
            "biaya",
            "tarif",
            "budget",
            "harganya"
        ],
        "answer": "Biaya bergantung pada tingkat kesulitan dan fitur yang dibutuhkan. Jelaskan kebutuhanmu terlebih dahulu, lalu aku akan membantu memperkirakan biaya yang sesuai."
    },

    "kontak": {
        "keywords": [
            "kontak",
            "wa",
            "whatsapp",
            "hubungi",
            "nomor",
            "email"
        ],
        "answer": "Jika ingin berdiskusi langsung dengan ARTUP STUDIO, kamu dapat menghubungi WhatsApp 0813-2834-3908 atau email p1998mr@gmail.com."
    },

    "otomatisasi": {
        "keywords": [
            "otomatisasi",
            "automate",
            "bot",
            "chatbot",
            "buat bot"
        ],
        "answer": "Otomatisasi bisa menghemat banyak waktu. Jika kamu membutuhkan bot Telegram, chatbot AI, integrasi API, atau sistem otomatis lainnya, jelaskan kebutuhanmu dan aku akan membantu mengarahkannya."
    }
}




# =========================
# REQUEST MODEL
# =========================




# =========================
# MEMORY
# =========================

memory = {
    "last_topic": None,

    "stage": None,
    "service": None,
    "goal": None,
    "budget": None,
    "deadline": None,

    "lead_score": 0
}


class ChatRequest(BaseModel):
    message: str

# =========================
# LOGGING
# =========================

def log_chat(user_input, response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(
        "chat_history.txt",
        "a",
        encoding="utf-8"
    ) as f:
        f.write(
            f"[{timestamp}] User: {user_input} | AI: {response}\n"
        )

# =========================
# UTIL
# =========================

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text

# =========================
# LEAD DETECTOR
# =========================

lead_words = [
    "pesan",
    "order",
    "buat website",
    "mau website",
    "tertarik",
    "kerjasama",
    "bikin website"
]

# =========================
# INTENT MATCHER
# =========================

def find_best_topic(user_input):
    best_topic = None
    best_score = 0
    user_input = normalize(user_input)

    for topic, data in knowledge.items():
        # Buat list keyword sementara
        keywords_to_check = []
        
        # JIKA DATA ADALAH LIST (Kasus "status")
        if isinstance(data, list):
            for item in data:
                for kw in item.get("keywords", []):
                    keywords_to_check.append(kw)
        # JIKA DATA ADALAH DICTIONARY (Kasus lain)
        elif isinstance(data, dict):
             keywords_to_check = data.get("keywords", []);

        # Cek skor fuzz terhadap semua keyword yang dikumpulkan
        for keyword in keywords_to_check:
            score = fuzz.partial_ratio(user_input, keyword)
            if score > best_score:
                best_score = score
                best_topic = topic

    return best_topic, best_score
def reset_lead():
    memory["stage"] = None
    memory["service"] = None
    memory["goal"] = None
    memory["budget"] = None
    memory["deadline"] = None

# =========================
# CHAT ENGINE
# =========================
def generate_normal_response(user_input):

    user_input = normalize(user_input)

    for word in lead_words:
        if word in user_input:
            return (
                "Kalau kamu tertarik membuat project digital, "
                "coba jelaskan kebutuhanmu terlebih dahulu ya."
            )

    topic, score = find_best_topic(user_input)

    if topic and score >= 70:

        data = knowledge.get(topic)

        if isinstance(data, list):

            for item in data:
                for kw in item["keywords"]:
                    if kw in user_input:
                        return item["answer"]

            return (
                "Hm... aku kurang yakin memahami maksudmu. "
                "Bisakah dijelaskan sedikit lebih detail?"
            )

        elif isinstance(data, dict):

            return data.get(
                "answer",
                "Maaf, aku belum memiliki jawaban untuk itu."
            )

    return (
        "Hm... aku belum memahami pertanyaan itu. "
        "Aku bisa membantu seputar:\n\n"
        "• Jasa Website\n"
        "• Bot Telegram\n"
        "• Otomatisasi\n"
        "• Harga\n"
        "• Kontak ARTUP STUDIO\n\n"
        "Coba jelaskan kebutuhanmu lebih detail."
    )



def generate_response(user_input):
    user_input = normalize(user_input)

    # 0. LOGIKA BATAL/RESET (Penting agar user tidak terjebak)
    if "batal" in user_input or "reset" in user_input or "mulai lagi" in user_input:
        reset_lead()
        return "Oke, sesi dibatalkan. Ada lagi yang bisa saya bantu terkait Artup Studio?"

    # 1. LOGIKA "STATE" (Jika user sedang dalam proses memilih)
    if memory["stage"] == "pilih_jasa":
        if "landing" in user_input or "1" in user_input:
            memory["service"] = "Landing Page"
            memory["stage"] = "konfirmasi_pembayaran"
            return "Landing Page dipilih (Harga mulai Rp 100.000 - Rp 550.000). Apakah Anda berminat lanjut ke pembayaran?"
        elif "web" in user_input or "2" in user_input:
            memory["service"] = "Toko Online"
            memory["stage"] = "konfirmasi_pembayaran"
            return "pembuatan web dipilih (Harga mulai Rp 200.000 - Rp tergantung fungsi). Apakah Anda berminat lanjut ke pembayaran?"
        elif "toko" in user_input or "3" in user_input:
            memory["service"] = "Toko Online"
            memory["stage"] = "konfirmasi_pembayaran"
            return "Toko Online dipilih (Harga mulai Rp 200.000 - Rp tergantung fungsi). Apakah Anda berminat lanjut ke pembayaran?"
        elif "bot telegram" in user_input or "4" in user_input:
            memory["service"] = "Bot Chat Telegram"
            memory["stage"] = "konfirmasi_pembayaran"
            return "Bot Chat Telegram dipilih (Harga mulai Rp 50.000 - Rp tergantung fungsi). Apakah Anda berminat lanjut ke pembayaran?"
        elif "bot otomatisasi" in user_input or "5" in user_input:
            memory["service"] = "Bot Otomatisasi"
            memory["stage"] = "konfirmasi_pembayaran"
            return "Bot Otomatisasi dipilih (Harga mulai Rp 50.000 - Rp tergantung fungsi). Apakah Anda berminat lanjut ke pembayaran?"
        elif "diskusi" in user_input or "6" in user_input:
            reset_lead()
            return "Silahkan hubungi kontak kami via WhatsApp: 0813-2834-3908 untuk diskusi lebih lanjut."
    
    # Jika user setuju pembayaran
    if memory["stage"] == "konfirmasi_pembayaran" and ("iya" in user_input or "oke" in user_input or "ya" in user_input or "lanjut" in user_input):
        service_name = memory["service"]
        reset_lead() 
        return f"Terima kasih! Pesanan untuk {service_name} sudah dicatat. Silahkan hubungi kami di WA: 0813-2834-3908 untuk konfirmasi desain, fungsi dan pembayaran."

    # 2. LOGIKA TRIGGER AWAL (Jika user tanya jasa)
    # Gunakan fuzz matching untuk mendeteksi keinginan user melihat jasa
    topic, score = find_best_topic(user_input)
    
    if topic == "jasa" and score >= 70:
        memory["stage"] = "pilih_jasa"
        return """Kami punya beberapa pilihan jasa:
1. Landing Page

2. Website

3. Toko Online

4. Bot Chat Telegram

5. Bot Otomatisasi

6. Diskusi Kebutuhan digital


[Mana yang ingin Anda buat?]"""

    # 3. FALLBACK / NORMAL
    return generate_normal_response(user_input)


# =========================
# API
# =========================

@app.post("/chat")
async def chat(request: ChatRequest):

    try:

        response = generate_response(
            request.message
        )

        log_chat(
            request.message,
            response
        )

        return {
            "reply": response
        }

    except Exception as e:

        print("ERROR:", e)

        return {
            "reply":
            "E-Eh...? Sepertinya terjadi kesalahan saat memproses pesanmu. Coba kirim ulang atau gunakan kalimat yang berbeda."
        }