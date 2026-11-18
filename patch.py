import os, glob, sys, re, struct, zlib

print("[*] TNT V63 — icon + VN + stable crack")

# ===== Generate simple TNT-style PNG icon (no external deps) =====
def write_png(path, size=192):
    # solid red block with darker border + white TNT text approximation via pixels
    w = h = size
    raw = bytearray()
    for y in range(h):
        raw.append(0)  # filter none
        for x in range(w):
            # border gray
            border = 8
            if x < border or y < border or x >= w-border or y >= h-border:
                r,g,b = 90, 90, 90
            else:
                # red TNT body
                r,g,b = 200, 40, 40
                # middle white band
                band = h // 2
                if abs(y - band) < h // 10:
                    r,g,b = 230, 230, 230
                # top fuse dark
                if y < h // 4 and abs(x - w//2) < w // 8:
                    r,g,b = 40, 40, 40
            raw += bytes([r, g, b, 255])
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)

def install_icon():
    os.makedirs("green/res/drawable", exist_ok=True)
    write_png("/tmp/tnt_icon.png", 192)
    for root, dirs, files in os.walk("green/res"):
        for name in files:
            if name in ("brand_logo.png", "modjav_logo.png"):
                dest = os.path.join(root, name)
                open(dest, "wb").write(open("/tmp/tnt_icon.png", "rb").read())
                print("[OK] icon ->", dest)
    # ensure brand_logo exists
    dest = "green/res/drawable/brand_logo.png"
    open(dest, "wb").write(open("/tmp/tnt_icon.png", "rb").read())
    print("[OK] brand_logo.png")

install_icon()

# ===== SECURITY (same as working build) =====
for pattern in ["green/smali/**/IntegrityVerifier.smali", "green/smali_classes*/**/IntegrityVerifier.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        start = c.find(".method static verify(Ljava/io/File;[[BLjava/lang/String;)Z")
        if start != -1:
            nextm = c.find("\n.method ", start + 10)
            if nextm == -1: nextm = len(c)
            end = c.rfind(".end method", start, nextm)
            new = ".method static verify(Ljava/io/File;[[BLjava/lang/String;)Z\n    .registers 3\n    const/4 v0, 0x1\n    return v0\n.end method\n"
            with open(p, "w") as f: f.write(c[:start] + new + c[end+len(".end method"):])
            print("[OK] IntegrityVerifier")

for pattern in ["green/smali/**/ProtectedApplication.smali", "green/smali_classes*/**/ProtectedApplication.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        for sig, body in [
(".method public static trusted(Landroid/content/Context;)Z",
".method public static trusted(Landroid/content/Context;)Z\n    .registers 1\n    const/4 v0, 0x1\n    return v0\n.end method\n"),
(".method public static require(Landroid/app/Activity;)Z",
".method public static require(Landroid/app/Activity;)Z\n    .registers 1\n    const/4 v0, 0x1\n    return v0\n.end method\n")
]:
            start = c.find(sig)
            if start != -1:
                nextm = c.find("\n.method ", start + 10)
                if nextm == -1: nextm = len(c)
                end = c.rfind(".end method", start, nextm)
                c = c[:start] + body + c[end+len(".end method"):]
        with open(p, "w") as f: f.write(c)
        print("[OK] ProtectedApplication")

for pattern in ["green/smali/**/Gate.smali", "green/smali_classes*/**/Gate.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        c2 = c.replace("0x112a880", "0x757B12C00L")
        if c2 != c:
            with open(p, "w") as f: f.write(c2)
            print("[OK] Gate limit")
        else:
            start = c.find(".method public static grant(Landroid/content/Context;JJ)V")
            if start != -1:
                nextm = c.find("\n.method ", start + 10)
                if nextm == -1: nextm = len(c)
                end = c.rfind(".end method", start, nextm)
                new = """.method public static grant(Landroid/content/Context;JJ)V
    .registers 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;
    move-result-object v0
    sput-object v0, Lcom/zyon/jetkey/Gate;->context:Landroid/content/Context;
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J
    move-result-wide v0
    const-wide v2, 0x757B12C00L
    add-long/2addr v0, v2
    sput-wide v0, Lcom/zyon/jetkey/Gate;->until:J
    sput-wide p3, Lcom/zyon/jetkey/Gate;->expires:J
    sget-object v0, Lcom/zyon/jetkey/Gate;->handler:Landroid/os/Handler;
    sget-object v1, Lcom/zyon/jetkey/Gate;->tick:Ljava/lang/Runnable;
    invoke-virtual {v0, v1}, Landroid/os/Handler;->removeCallbacks(Ljava/lang/Runnable;)V
    invoke-virtual {v0, v1}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z
    return-void
.end method
"""
                with open(p, "w") as f: f.write(c[:start] + new + c[end+len(".end method"):])
                print("[OK] Gate.grant")

for pattern in ["green/smali/**/TicketVerifier.smali", "green/smali_classes*/**/TicketVerifier.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        start = c.find(".method public static verify(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;J)J")
        if start == -1:
            start = c.find(".method static verify(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;J)J")
        if start != -1:
            nextm = c.find("\n.method ", start + 10)
            if nextm == -1: nextm = len(c)
            end = c.rfind(".end method", start, nextm)
            new = """.method public static verify(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;J)J
    .registers 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation
    const-wide v0, 0x757B12C00L
    return-wide v0
.end method
"""
            with open(p, "w") as f: f.write(c[:start] + new + c[end+len(".end method"):])
            print("[OK] TicketVerifier")

for pattern in ["green/smali/**/LoginActivity.smali", "green/smali_classes*/**/LoginActivity.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        start = c.find(".method private login()V")
        if start != -1:
            nextm = c.find("\n.method ", start + 10)
            if nextm == -1: nextm = len(c)
            end = c.rfind(".end method", start, nextm)
            new = """.method private login()V
    .registers 8
    const-wide v0, 0x757B12C00L
    const-wide v2, 0x7FFFFFFFFFFFFFFFL
    :try_start_0
    invoke-static {p0, v0, v1, v2, v3}, Lcom/zyon/jetkey/Gate;->grant(Landroid/content/Context;JJ)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0
    new-instance v4, Landroid/content/Intent;
    invoke-direct {v4}, Landroid/content/Intent;-><init>()V
    invoke-virtual {p0}, Lcom/zyon/jetkey/LoginActivity;->getPackageName()Ljava/lang/String;
    move-result-object v5
    new-instance v6, Ljava/lang/StringBuilder;
    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V
    invoke-virtual {v6, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v5, ".MainActivity"
    invoke-virtual {v6, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v5
    invoke-virtual {v4, p0, v5}, Landroid/content/Intent;->setClassName(Landroid/content/Context;Ljava/lang/String;)Landroid/content/Intent;
    invoke-virtual {p0, v4}, Lcom/zyon/jetkey/LoginActivity;->startActivity(Landroid/content/Intent;)V
    invoke-virtual {p0}, Lcom/zyon/jetkey/LoginActivity;->finish()V
    return-void
    :catch_0
    move-exception v0
    return-void
.end method
"""
            with open(p, "w") as f: f.write(c[:start] + new + c[end+len(".end method"):])
            print("[OK] LoginActivity")

# ===== VN =====
replacements = [
    ("Digite TNT e os seis números da key.", "Nhập key bất kỳ rồi bấm Vào Menu."),
    ("Validando sua key dentro do aplicativo…", "Đang xác thực key…"),
    ("Key recebida. Toque em Entrar no painel.", "Đã nhận key. Bấm Vào Menu."),
    ("Confirmação inválida ou expirada. Toque em Entrar novamente.", "Xác nhận lỗi. Thử lại."),
    ("Validação cancelada. Você pode tentar novamente.", "Đã hủy. Thử lại."),
    ("Instale ou ative o Google Chrome para gerar sua key.", "Cần Chrome để tạo key."),
    ("ENTRAR NO PAINEL", "▶  VÀO MENU"),
    ("GERAR KEY", "✦  TẠO KEY"),
    ("Sejam bem-vindos ao TNT APK V63!", "Chào mừng TNT APK V63"),
    ("KEY ATIVA", "KEY ĐANG HOẠT ĐỘNG"),
    ("restantes", "còn lại"),
    ("Expira em", "Hết hạn lúc"),
    ("Key expirada. Gere uma nova key.", "Key hết hạn. Tạo key mới."),
    ("Acesso expirado.", "Truy cập hết hạn."),
    ("Integridade inválida. Instale o APK original do criador.", "Lỗi tích hợp."),
    ("Não foi possível validar. Confira sua conexão e tente novamente.", "Không xác thực được. Kiểm tra mạng."),
    ("Não foi possível abrir a tela principal.", "Không mở được màn hình chính."),
    ("Não foi possível abrir o link. Verifique seu navegador.", "Không mở được link."),
    ("Atualização disponível", "Có bản cập nhật"),
    ("Atualizar", "Cập nhật"),
    ("Sair", "Thoát"),
    ("Instalar", "Cài đặt"),
    ("INSTALAR", "CÀI ĐẶT"),
    ("Launch", "Mở game"),
    ("LAUNCH", "MỞ GAME"),
    ("Iniciar", "Khởi động"),
    ("Pronto", "Sẵn sàng"),
    ("Aguardando", "Đang chờ"),
    ("Conectado", "Đã kết nối"),
    ("Desconectado", "Mất kết nối"),
    ("Erro", "Lỗi"),
    ("Sucesso", "Thành công"),
    ("Carregando", "Đang tải"),
    ("Processando", "Đang xử lý"),
    ("Concluído", "Hoàn thành"),
    ("Falhou", "Thất bại"),
    ("Tentar novamente", "Thử lại"),
    ("Cancelar", "Hủy"),
    ("Confirmar", "Xác nhận"),
    ("Fechar", "Đóng"),
    ("Pareamento", "Ghép nối"),
    ("Parear", "Ghép nối"),
    ("Depuração sem fio", "Gỡ lỗi không dây"),
    ("Código de pareamento", "Mã ghép nối"),
    ("Módulo", "Module"),
    ("Instalando módulo", "Đang cài module"),
    ("Módulo instalado", "Module đã cài"),
    ("Falha na instalação", "Cài đặt thất bại"),
    ("Arquivo não encontrado", "Không tìm thấy file"),
    ("Permissão negada", "Bị từ chối quyền"),
    ("Permissão", "Quyền"),
    ("Configurações", "Cài đặt"),
    ("Opções", "Tùy chọn"),
    ("Ativar", "Bật"),
    ("Desativar", "Tắt"),
    ("Ligado", "Bật"),
    ("Desligado", "Tắt"),
    ("Limite de usos atingido", "Đã hết lượt"),
    ("Key inválida", "Key không hợp lệ"),
    ("Conexão perdida", "Mất kết nối"),
    ("Tempo esgotado", "Hết thời gian"),
    ("Falha na conexão", "Kết nối thất bại"),
    ("Sem internet", "Không có mạng"),
    ("Verifique sua conexão", "Kiểm tra mạng"),
    ("Tente novamente mais tarde", "Thử lại sau"),
    ("Algo deu errado", "Đã xảy ra lỗi"),
    ("Operação cancelada", "Đã hủy"),
    ("Aguarde", "Vui lòng đợi"),
    ("Acesso", "Truy cập"),
    ("Licença", "Key"),
    ("Licenca", "Key"),
    ("Painel", "Bảng điều khiển"),
    ("Versão", "Phiên bản"),
    ("Sobre", "Giới thiệu"),
    ("Ajuda", "Trợ giúp"),
    ("Suporte", "Hỗ trợ"),
    ("Canal", "Kênh"),
    ("Grupo", "Nhóm"),
    ("Baixar", "Tải xuống"),
    ("Atualizado", "Đã cập nhật"),
    ("Novo", "Mới"),
    ("Estável", "Ổn định"),
]

def translate_const_strings(content, pairs):
    def replacer(m):
        full = m.group(0)
        q1, q2 = full.find('"'), full.rfind('"')
        if q1 < 0 or q2 <= q1: return full
        prefix, s, suffix = full[:q1+1], full[q1+1:q2], full[q2:]
        for old, new in pairs:
            if old in s: s = s.replace(old, new)
        return prefix + s + suffix
    return re.sub(r'const-string(?:/jumbo)?\s+v\d+,\s*".*?"', replacer, content)

count = 0
for root, dirs, files in os.walk("green"):
    for name in files:
        if not name.endswith(".smali"): continue
        full = os.path.join(root, name)
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f: content = f.read()
            newc = translate_const_strings(content, replacements)
            if newc != content:
                with open(full, "w", encoding="utf-8") as f: f.write(newc)
                count += 1
        except Exception: pass
print(f"[OK] VN ({count} files)")
print("[*] Done")
