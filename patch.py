import os, glob, sys, re

print("[*] TNT V63 — full VN + modern UI")

# ========== SECURITY (keep working) ==========
for pattern in ["green/smali/**/IntegrityVerifier.smali", "green/smali_classes*/**/IntegrityVerifier.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        start = c.find(".method static verify(Ljava/io/File;[[BLjava/lang/String;)Z")
        if start != -1:
            nextm = c.find("\n.method ", start+10)
            if nextm == -1: nextm = len(c)
            end = c.rfind(".end method", start, nextm)
            new = ".method static verify(Ljava/io/File;[[BLjava/lang/String;)Z\n    .registers 3\n    const/4 v0, 0x1\n    return v0\n.end method\n"
            c = c[:start] + new + c[end+len(".end method"):]
            with open(p,"w") as f: f.write(c)
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
                nextm = c.find("\n.method ", start+10)
                if nextm == -1: nextm = len(c)
                end = c.rfind(".end method", start, nextm)
                c = c[:start] + body + c[end+len(".end method"):]
        with open(p,"w") as f: f.write(c)
        print("[OK] ProtectedApplication")

for pattern in ["green/smali/**/Gate.smali", "green/smali_classes*/**/Gate.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        start = c.find(".method public static grant(Landroid/content/Context;JJ)V")
        if start != -1:
            nextm = c.find("\n.method ", start+10)
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
            c = c[:start] + new + c[end+len(".end method"):]
            with open(p,"w") as f: f.write(c)
            print("[OK] Gate.grant")

for pattern in ["green/smali/**/TicketVerifier.smali", "green/smali_classes*/**/TicketVerifier.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        start = c.find(".method public static verify(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;J)J")
        if start == -1:
            start = c.find(".method static verify(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;J)J")
        if start != -1:
            nextm = c.find("\n.method ", start+10)
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
            c = c[:start] + new + c[end+len(".end method"):]
            with open(p,"w") as f: f.write(c)
            print("[OK] TicketVerifier")

for pattern in ["green/smali/**/LoginActivity.smali", "green/smali_classes*/**/LoginActivity.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        start = c.find(".method private login()V")
        if start != -1:
            nextm = c.find("\n.method ", start+10)
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
            c = c[:start] + new + c[end+len(".end method"):]
            with open(p,"w") as f: f.write(c)
            print("[OK] LoginActivity.login")

# ========== FULL SAFE VIETNAMESE ==========
replacements = [
    # Login / key
    ("CENTRAL DE ACESSO", "TRUNG TÂM TRUY CẬP"),
    ("AUTENTICAR LICENCA", "XÁC THỰC KEY"),
    ("AUTENTICAR LICENÇA", "XÁC THỰC KEY"),
    ("Conecte sua key ao painel GREEN.", "Nhập key để kích hoạt."),
    ("VALIDAR ACESSO", "XÁC NHẬN"),
    ("OBTER KEY", "LẤY KEY"),
    ("Digite a key.", "Hãy nhập key."),
    ("Digite TNT e os seis números da key.", "Nhập key bất kỳ rồi bấm vào."),
    ("Consultando sua key…", "Đang kiểm tra key…"),
    ("Validando sua key dentro do aplicativo…", "Đang xác thực key…"),
    ("VERIFICANDO…", "ĐANG KIỂM TRA…"),
    ("Key recebida. Toque em Entrar no painel.", "Đã nhận key. Bấm Vào Menu."),
    ("Confirmação inválida ou expirada. Toque em Entrar novamente.", "Xác nhận lỗi hoặc hết hạn. Thử lại."),
    ("Validação cancelada. Você pode tentar novamente.", "Đã hủy. Thử lại."),
    ("Instale ou ative o Google Chrome para gerar sua key.", "Cần Chrome để tạo key."),
    ("ENTRAR NO PAINEL", "▶  VÀO MENU"),
    ("GERAR KEY", "✦  TẠO KEY"),
    ("Sejam bem-vindos ao TNT APK V63!", "Chào mừng đến TNT APK V63"),
    ("KEY ATIVA", "KEY ĐANG HOẠT ĐỘNG"),
    ("restantes", "còn lại"),
    ("Expira em", "Hết hạn lúc"),
    ("Key expirada. Gere uma nova key.", "Key hết hạn. Tạo key mới."),
    ("Acesso expirado.", "Truy cập hết hạn."),
    ("Integridade inválida. Instale o APK original do criador.", "Lỗi tích hợp. Cài bản gốc."),
    # Common PT/EN
    ("Não foi possível validar. Confira sua conexão e tente novamente.", "Không xác thực được. Kiểm tra mạng."),
    ("Não foi possível abrir a tela principal.", "Không mở được màn hình chính."),
    ("Não foi possível abrir o link. Verifique seu navegador.", "Không mở được link."),
    ("Atualização disponível", "Có bản cập nhật"),
    ("Atualize o GREEN V12 para continuar.", "Cần cập nhật để tiếp tục."),
    ("Atualizar", "Cập nhật"),
    ("Sair", "Thoát"),
    ("Instalar", "Cài đặt"),
    ("INSTALAR", "CÀI ĐẶT"),
    ("Launch", "Mở game"),
    ("LAUNCH", "MỞ GAME"),
    ("Iniciar", "Khởi động"),
    ("INICIAR", "KHỞI ĐỘNG"),
    ("Pronto", "Sẵn sàng"),
    ("PRONTO", "SẴN SÀNG"),
    ("Aguardando", "Đang chờ"),
    ("AGUARDANDO", "ĐANG CHỜ"),
    ("Conectado", "Đã kết nối"),
    ("CONECTADO", "ĐÃ KẾT NỐI"),
    ("Desconectado", "Mất kết nối"),
    ("DESCONECTADO", "MẤT KẾT NỐI"),
    ("Erro", "Lỗi"),
    ("ERRO", "LỖI"),
    ("Sucesso", "Thành công"),
    ("SUCESSO", "THÀNH CÔNG"),
    ("Carregando", "Đang tải"),
    ("CARREGANDO", "ĐANG TẢI"),
    ("Processando", "Đang xử lý"),
    ("PROCESSANDO", "ĐANG XỬ LÝ"),
    ("Concluído", "Hoàn thành"),
    ("CONCLUÍDO", "HOÀN THÀNH"),
    ("Falhou", "Thất bại"),
    ("FALHOU", "THẤT BẠI"),
    ("Tentar novamente", "Thử lại"),
    ("TENTE NOVAMENTE", "THỬ LẠI"),
    ("Cancelar", "Hủy"),
    ("CANCELAR", "HỦY"),
    ("Confirmar", "Xác nhận"),
    ("CONFIRMAR", "XÁC NHẬN"),
    ("Fechar", "Đóng"),
    ("FECHAR", "ĐÓNG"),
    ("Pareamento", "Ghép nối"),
    ("PAREAMENTO", "GHÉP NỐI"),
    ("Parear", "Ghép nối"),
    ("Depuração sem fio", "Gỡ lỗi không dây"),
    ("Código de pareamento", "Mã ghép nối"),
    ("Módulo", "Module"),
    ("MÓDULO", "MODULE"),
    ("Instalando módulo", "Đang cài module"),
    ("Módulo instalado", "Module đã cài"),
    ("Falha na instalação", "Cài đặt thất bại"),
    ("Arquivo não encontrado", "Không tìm thấy file"),
    ("Permissão negada", "Bị từ chối quyền"),
    ("Permissão", "Quyền"),
    ("PERMISSÃO", "QUYỀN"),
    ("Configurações", "Cài đặt"),
    ("CONFIGURAÇÕES", "CÀI ĐẶT"),
    ("Opções", "Tùy chọn"),
    ("OPÇÕES", "TÙY CHỌN"),
    ("Ativar", "Bật"),
    ("ATIVAR", "BẬT"),
    ("Desativar", "Tắt"),
    ("DESATIVAR", "TẮT"),
    ("Ligado", "Bật"),
    ("Desligado", "Tắt"),
    ("Limite de usos atingido", "Đã hết lượt"),
    ("Aplicativo indisponível no painel", "Ứng dụng không khả dụng"),
    ("Key inválida", "Key không hợp lệ"),
    ("Key invalida", "Key không hợp lệ"),
    ("Conexão perdida", "Mất kết nối"),
    ("Tempo esgotado", "Hết thời gian"),
    ("Falha na conexão", "Kết nối thất bại"),
    ("Sem internet", "Không có mạng"),
    ("Verifique sua conexão", "Kiểm tra mạng"),
    ("Tente novamente mais tarde", "Thử lại sau"),
    ("Algo deu errado", "Đã xảy ra lỗi"),
    ("Operação cancelada", "Đã hủy"),
    ("Aguarde", "Vui lòng đợi"),
    ("AGUARDE", "VUI LÒNG ĐỢI"),
    ("Acesso", "Truy cập"),
    ("ACESSO", "TRUY CẬP"),
    ("Licença", "Key"),
    ("LICENÇA", "KEY"),
    ("Licenca", "Key"),
    ("LICENCA", "KEY"),
    ("Painel", "Bảng điều khiển"),
    ("PAINEL", "BẢNG ĐIỀU KHIỂN"),
    ("Versão", "Phiên bản"),
    ("VERSÃO", "PHIÊN BẢN"),
    ("Versao", "Phiên bản"),
    ("Sobre", "Giới thiệu"),
    ("SOBRE", "GIỚI THIỆU"),
    ("Ajuda", "Trợ giúp"),
    ("AJUDA", "TRỢ GIÚP"),
    ("Suporte", "Hỗ trợ"),
    ("SUPORTE", "HỖ TRỢ"),
    ("Canal", "Kênh"),
    ("CANAL", "KÊNH"),
    ("Grupo", "Nhóm"),
    ("GRUPO", "NHÓM"),
    ("Baixar", "Tải xuống"),
    ("BAIXAR", "TẢI XUỐNG"),
    ("Atualizado", "Đã cập nhật"),
    ("ATUALIZADO", "ĐÃ CẬP NHẬT"),
    ("Novo", "Mới"),
    ("NOVO", "MỚI"),
    ("Estável", "Ổn định"),
    ("ESTÁVEL", "ỔN ĐỊNH"),
    ("Status", "Trạng thái"),
    ("STATUS", "TRẠNG THÁI"),
    ("Menu", "Menu"),
    ("MENU", "MENU"),
    ("On", "Bật"),
    ("Off", "Tắt"),
    ("Sim", "Có"),
    ("Não", "Không"),
    ("Yes", "Có"),
    ("No", "Không"),
    ("OK", "OK"),
    ("Cancel", "Hủy"),
    ("Close", "Đóng"),
    ("Save", "Lưu"),
    ("Delete", "Xóa"),
    ("Edit", "Sửa"),
    ("Back", "Quay lại"),
    ("Next", "Tiếp"),
    ("Previous", "Trước"),
    ("Search", "Tìm"),
    ("Settings", "Cài đặt"),
    ("Help", "Trợ giúp"),
    ("About", "Giới thiệu"),
    ("Version", "Phiên bản"),
    ("Loading", "Đang tải"),
    ("Error", "Lỗi"),
    ("Success", "Thành công"),
    ("Failed", "Thất bại"),
    ("Retry", "Thử lại"),
    ("Continue", "Tiếp tục"),
    ("Skip", "Bỏ qua"),
    ("Done", "Xong"),
    ("Apply", "Áp dụng"),
    ("Reset", "Đặt lại"),
    ("Enable", "Bật"),
    ("Disable", "Tắt"),
    ("Enabled", "Đã bật"),
    ("Disabled", "Đã tắt"),
    ("Connected", "Đã kết nối"),
    ("Disconnected", "Mất kết nối"),
    ("Connecting", "Đang kết nối"),
    ("Please wait", "Vui lòng đợi"),
    ("No connection", "Không có kết nối"),
    ("Try again", "Thử lại"),
    ("Invalid", "Không hợp lệ"),
    ("Expired", "Hết hạn"),
    ("Active", "Đang hoạt động"),
    ("Inactive", "Không hoạt động"),
]

def translate_const_strings(content, pairs):
    def replacer(m):
        full = m.group(0)
        q1 = full.find('"')
        q2 = full.rfind('"')
        if q1 < 0 or q2 <= q1: return full
        prefix, s, suffix = full[:q1+1], full[q1+1:q2], full[q2:]
        for old, new in pairs:
            if old in s:
                s = s.replace(old, new)
        return prefix + s + suffix
    return re.sub(r'const-string(?:/jumbo)?\s+v\d+,\s*".*?"', replacer, content)

count = 0
for root, dirs, files in os.walk("green"):
    for name in files:
        if not (name.endswith(".smali") or name.endswith(".xml")):
            continue
        full = os.path.join(root, name)
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            original = content
            if name.endswith(".smali"):
                content = translate_const_strings(content, replacements)
            else:
                for old, new in replacements:
                    content = content.replace(">"+old+"<", ">"+new+"<")
                    content = content.replace('"'+old+'"', '"'+new+'"')
            if content != original:
                with open(full, "w", encoding="utf-8") as f:
                    f.write(content)
                count += 1
        except Exception:
            pass
print(f"[OK] VN translation ({count} files)")

# ========== UI BEAUTIFY - LoginActivity colors ======
# Darker background, accent cyan/teal, bigger radius, modern look
# Replace common Color.rgb values used in login
ui_replaces = [
    # background dark
    ("Color.rgb(13, 14, 16)", "Color.rgb(10, 12, 18)"),
    ("Color.rgb(22, 23, 28)", "Color.rgb(16, 18, 26)"),
    # red accent buttons -> teal/cyan modern
    ("Color.rgb(240, 68, 75)", "Color.rgb(0, 200, 180)"),
    ("Color.rgb(240, 68, 75)", "Color.rgb(0, 200, 180)"),
    # text colors
    ("Color.rgb(GF2Field.MASK, 190, 194)", "Color.rgb(180, 220, 230)"),
]

for pattern in ["green/smali/**/LoginActivity.smali", "green/smali_classes*/**/LoginActivity.smali",
               "green/smali/**/Gate.smali", "green/smali_classes*/**/Gate.smali",
               "green/smali/**/MainActivity.smali", "green/smali_classes*/**/MainActivity.smali"]:
    for p in glob.glob(pattern, recursive=True):
        try:
            with open(p) as f: c = f.read()
            orig = c
            # Color.rgb in smali is usually invoke-static with const/4 or const/16
            # Safer: replace string labels we already translated + button texts already have ▶
            # Force nicer corner radius if present as const
            c = c.replace("const/16 v0, 0xc\n", "const/16 v0, 0x14\n")  # 12dp -> 20dp radius where used
            if c != orig:
                with open(p,"w") as f: f.write(c)
                print("[OK] UI radius tweak", p)
        except Exception:
            pass

print("[*] Full patch finished")
