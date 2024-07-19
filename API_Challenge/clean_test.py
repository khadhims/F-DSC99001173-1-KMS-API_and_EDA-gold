import re

def verify_and_clean_text(text):
    # Dekode teks jika dalam bentuk byte
    text = text.encode().decode('unicode_escape')
    
    # Pola regex untuk memverifikasi bahwa teks hanya berisi huruf dan spasi
    verify_pattern = r'^[a-zA-Z\s]+$'

    # Pola regex untuk menghapus angka dan simbol (kecuali huruf dan spasi)
    clean_pattern = r'[^a-zA-Z\s]'

    # Verifikasi teks
    if re.fullmatch(verify_pattern, text):
        print("Text only contains letters and spaces.")
    else:
        print("Text contains other characters.")

    # Bersihkan teks dari angka dan simbol
    cleaned_text = re.sub(clean_pattern, '', text)

    return cleaned_text

# Contoh penggunaan
input_text = "\xf0\x9f\x98\x84\xf0\x9f\x98\x84\xf0\x9f\x98\x84' Ini adalah contoh1 kalimat2 /dengan angka3 & simbol lainnya."
cleaned_text = verify_and_clean_text(input_text)
print(f"Input : '{input_text}'")   
print(f"Output : '{cleaned_text}'")