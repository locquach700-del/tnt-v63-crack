import os, glob, sys, re

print("[*] TNT V63 crack + full VN (safe)")

# ===== 1. IntegrityVerifier.verify -> true =====
for pattern in ["green/smali/**/IntegrityVerifier.smali", "green/smali_classes*/**/IntegrityVerifier.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        start = c.find(".method static verify(Ljava/io/File;[[BLjava/lang/String;)Z")
        if start != -1:
            nextm = c.find("\n.method ", start + 10)
            if nextm == -1: nextm = len(c)
            end = c.rfind(".end method", start, nextm)
            new = """.method static verify(Ljava/io/File;[[BLjava/lang/String;)Z
    .registers 3
    const/4 v0, 0x1
    return v0
.end method
"""
            c = c[:start] + new + c[end+len(".end method"):]
            with open(p,"w") as f: f.write(c)
            print("[OK] IntegrityVerifier", p)

# ===== 2. ProtectedApplication.trusted + require -> true =====
for pattern in ["green/smali/**/ProtectedApplication.smali", "green/smali_classes*/**/ProtectedApplication.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        for sig, body in [
(".method public static trusted(Landroid/content/Context;)Z",
""".method public static trusted(Landroid/content/Context;)Z
    .registers 1
    const/4 v0, 0x1
    return v0
.end method
"""),
(".method public static require(Landroid/app/Activity;)Z",
""".method public static require(Landroid/app/Activity;)Z
    .registers 1
    const/4 v0, 0x1
    return v0
.end method
""")
]:
            start = c.find(sig)
            if start != -1:
                nextm = c.find("\n.method ", start+10)
                if nextm == -1: nextm = len(c)
                end = c.rfind(".end method", start, nextm)
                c = c[:start] + body + c[end+len(".end method"):]
        with open(p,"w") as f: f.write(c)
        print("[OK] ProtectedApplication", p)

# ===== 3. Gate.grant - remove max limit so long sessions work =====
for pattern in ["green/smali/**/Gate.smali", "green/smali_classes*/**/Gate.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f: c = f.read()
        # remove the upper bound check: if (j <= 0 || j > 18000000) throw
        # simplest: replace grant method body to always set long until
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

    # context = context2.getApplicationContext()
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;
    move-result-object v0
    sput-object v0, Lcom/zyon/jetkey/Gate;->context:Landroid/content/Context;

    # until = SystemClock.elapsedRealtime() + 31536000000L  (~1 year)
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J
    move-result-wide v0
    const-wide v2, 0x757B12C00L
    add-long/2addr v0, v2
    sput-wide v0, Lcom/zyon/jetkey/Gate;->until:J

    # expires = j2 (or far future)
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
            print("[OK] Gate.grant unlimited", p)

# ===== 4. TicketVerifier.verify -> always long remaining =====
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
            print("[OK] TicketVerifier", p)

# ===== 5. LoginActivity.login - force accept any key (including 1) =====
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
            print("[OK] LoginActivity.login forced", p)

print("[*] Security patches done")

# ===== 6. Safe full Vietnamese - ONLY const-string =====
replacements = [
    ("CENTRAL DE ACESSO", "TRUNG TÂM TRUY CẬP"),
    ("AUTENTICAR LICENCA", "XÁC THỰC KEY"),
    ("AUTENTICAR LICENÇA", "XÁC THỰC KEY"),
    ("Conecte sua key ao painel GREEN.", "Nhập key để kích hoạt."),
    ("VALIDAR ACESSO", "XÁC NHẬN"),
    ("OBTER KEY", "LẤY KEY"),
    ("Digite a key.", "Hãy nhập key."),
    ("Digite TNT e os seis números da key.", "Nhập key (TNT + 6 số hoặc bất kỳ)."),
    ("Consultando sua key…", "Đang kiểm tra key…"),
    ("Validando sua key dentro do aplicativo…", "Đang xác thực key…"),
    ("VERIFICANDO…", "ĐANG KIỂM TRA…"),
    ("Key recebida. Toque em Entrar no painel.", "Đã nhận key. Bấm Enter để vào."),
    ("Confirmação inválida ou expirada. Toque em Entrar novamente.", "Xác nhận không hợp lệ hoặc hết hạn. Thử lại."),
    ("Validação cancelada. Você pode tentar novamente.", "Đã hủy xác thực. Thử lại."),
    ("Instale ou ative o Google Chrome para gerar sua key.", "Cài hoặc bật Chrome để tạo key."),
    ("ENTRAR NO PAINEL", "VÀO MENU"),
    ("GERAR KEY", "TẠO KEY"),
    ("Sejam bem-vindos ao TNT APK V63!", "Chào mừng đến TNT APK V63!"),
    ("KEY ATIVA", "KEY ĐANG HOẠT ĐỘNG"),
    ("restantes", "còn lại"),
    ("Expira em", "Hết hạn lúc"),
    ("Key expirada. Gere uma nova key.", "Key đã hết hạn. Tạo key mới."),
    ("Acesso expirado.", "Truy cập đã hết hạn."),
    ("Integridade inválida. Instale o APK original do criador.", "Lỗi tích hợp. Cài bản gốc từ tác giả."),
    ("Não foi possível validar. Confira sua conexão e tente novamente.", "Không thể xác thực. Kiểm tra mạng."),
    ("Não foi possível abrir a tela principal.", "Không thể mở màn hình chính."),
    ("Não foi possível abrir o link. Verifique seu navegador.", "Không thể mở link."),
    ("Atualização disponível", "Có bản cập nhật"),
    ("Atualize o GREEN V12 para continuar.", "Cập nhật để tiếp tục."),
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
    ("Limite de usos atingido", "Đã hết lượt sử dụng"),
    ("Aplicativo indisponível no painel", "Ứng dụng không khả dụng"),
    ("Key inválida", "Key không hợp lệ"),
    ("Conexão perdida", "Mất kết nối"),
    ("Tempo esgotado", "Hết thời gian"),
    ("Falha na conexão", "Kết nối thất bại"),
    ("Sem internet", "Không có mạng"),
    ("Verifique sua conexão", "Kiểm tra kết nối mạng"),
    ("Tente novamente mais tarde", "Thử lại sau"),
    ("Algo deu errado", "Đã xảy ra lỗi"),
    ("Operação cancelada", "Đã hủy thao tác"),
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
                # only replace in xml string values, avoid attribute names
                for old, new in replacements:
                    content = content.replace(">"+old+"<", ">"+new+"<")
                    content = content.replace('"'+old+'"', '"'+new+'"')
            if content != original:
                with open(full, "w", encoding="utf-8") as f:
                    f.write(content)
                count += 1
        except Exception:
            pass

print(f"[OK] Safe VN translation ({count} files)")
print("[*] All done")
