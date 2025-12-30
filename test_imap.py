import imaplib, sys

print("Versión de Python:", sys.version)
print("Fichero de imaplib:", imaplib.__file__)
print("Atributos IMAP4*:", [name for name in dir(imaplib) if "IMAP4" in name])
print("Tiene IMAP4_SSL?:", hasattr(imaplib, "IMAP4_SSL"))
