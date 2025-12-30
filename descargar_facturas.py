import imaplib
import email
from email.header import decode_header
import os

# ============= CONFIGURACIÓN =============

IMAP_SERVER = "imap.gmail.com"      # Servidor IMAP de Gmail
IMAP_PORT = 993                     # Puerto IMAP sobre SSL

EMAIL_USER = "francisco.rosales.fernandez3@gmail.com"  # pon aquí tu gmail
EMAIL_PASS = "cihv oqwc zqjl vkmx"    # contraseña de aplicación de Google

DOWNLOAD_FOLDER = r"C:\prog\Py\Py_Prueba1"  # Carpeta donde guardar adjuntos
KEYWORD = "factura"                         # Palabra a buscar en los correos

# ========================================


def ensure_folder(path: str) -> None:
    """Crea la carpeta de destino si no existe."""
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def decode_str(s: str) -> str:
    """Decodifica cadenas codificadas en cabeceras (ej. asunto, nombres de adjuntos)."""
    if not s:
        return ""
    parts = decode_header(s)
    decoded = []
    for text, enc in parts:
        if isinstance(text, bytes):
            decoded.append(text.decode(enc or "utf-8", errors="ignore"))
        else:
            decoded.append(text)
    return "".join(decoded)


def sanitize_filename(filename: str, replacement: str = "_") -> str:
    # Sustituye caracteres prohibidos en Windows: \ / : * ? " < > |
    invalid_chars = '<>:"/\\|?*'
    cleaned = "".join(
        (c if c not in invalid_chars else replacement) for c in filename
    )
    # Quitar espacios y puntos al final
    cleaned = cleaned.rstrip(" .")

    if not cleaned:
        cleaned = "adjunto"

    # Limitar longitud máxima del nombre
    max_len = 200
    if len(cleaned) > max_len:
        root, ext = os.path.splitext(cleaned)
        cleaned = root[: max_len - len(ext)] + ext

    return cleaned


def connect_imap() -> imaplib.IMAP4_SSL:
    """Establece conexión IMAP y hace login en Gmail."""
    print("Conectando a Gmail por IMAP...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_USER, EMAIL_PASS)
    print("Login correcto.")
    return mail


def search_messages(mail: imaplib.IMAP4_SSL, keyword: str):
    """
    Busca mensajes que contengan 'keyword'.
    Si quisieras solo no leídos: mail.search(None, 'UNSEEN', 'TEXT', f'"{keyword}"')
    """
    status, _ = mail.select("INBOX")  # selecciona bandeja de entrada
    if status != "OK":
        print("No se pudo seleccionar INBOX")
        return []

    status, data = mail.search(None, 'TEXT', f'"{keyword}"')
    if status != "OK":
        print("Error en la búsqueda IMAP")
        return []

    msg_ids = data[0].split()  # lista de ids en bytes
    return msg_ids


def download_attachments_from_message(mail: imaplib.IMAP4_SSL, msg_id: bytes) -> None:
    """Descarga todos los adjuntos del mensaje cuyo id se pasa."""
    status, data = mail.fetch(msg_id, "(RFC822)")
    if status != "OK":
        print(f"No se pudo obtener el mensaje {msg_id.decode(errors='ignore')}")
        return

    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    subject = decode_str(msg.get("Subject", ""))
    print(f"Procesando mensaje: {subject}")

    if not msg.is_multipart():
        return

    for part in msg.walk():
        content_disposition = part.get("Content-Disposition", "") or ""
        if "attachment" not in content_disposition.lower():
            continue

        filename = part.get_filename()
        if not filename:
            continue

        filename = decode_str(filename)
        filename = sanitize_filename(filename)

        save_path = os.path.join(DOWNLOAD_FOLDER, filename)

        # Evitar sobreescribir archivos existentes
        base, ext = os.path.splitext(save_path)
        i = 1
        while os.path.exists(save_path):
            save_path = f"{base}_{i}{ext}"
            i += 1

        payload = part.get_payload(decode=True)
        if payload is None:
            continue

        with open(save_path, "wb") as f:
            f.write(payload)

        print(f"Adjunto guardado: {save_path}")


def main() -> None:
    print("Iniciando script de descarga de facturas...")
    ensure_folder(DOWNLOAD_FOLDER)

    mail = connect_imap()
    try:
        msg_ids = search_messages(mail, KEYWORD)
        print(f"Encontrados {len(msg_ids)} mensajes con la palabra '{KEYWORD}'.")

        for msg_id in msg_ids:
            download_attachments_from_message(mail, msg_id)
    finally:
        try:
            mail.close()
        except Exception:
            pass
        mail.logout()
        print("Conexión IMAP cerrada.")


if __name__ == "__main__":
    main()
