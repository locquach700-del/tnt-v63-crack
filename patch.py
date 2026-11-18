import os, glob, sys, re

print("[*] TNT V63 crack patcher")

# ===== 1. IntegrityVerifier.verify -> always true =====
for pattern in ["green/smali/**/IntegrityVerifier.smali", "green/smali_classes*/**/IntegrityVerifier.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f:
            c = f.read()
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
            c = c[:start] + new + c[end + len(".end method"):]
            with open(p, "w") as f:
                f.write(c)
            print("[OK] IntegrityVerifier", p)

# ===== 2. ProtectedApplication.trusted + require -> always true =====
for pattern in ["green/smali/**/ProtectedApplication.smali", "green/smali_classes*/**/ProtectedApplication.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f:
            c = f.read()
        # trusted
        start = c.find(".method public static trusted(Landroid/content/Context;)Z")
        if start != -1:
            nextm = c.find("\n.method ", start + 10)
            if nextm == -1: nextm = len(c)
            end = c.rfind(".end method", start, nextm)
            new = """.method public static trusted(Landroid/content/Context;)Z
    .registers 1
    const/4 v0, 0x1
    return v0
.end method
"""
            c = c[:start] + new + c[end + len(".end method"):]
        # require
        start = c.find(".method public static require(Landroid/app/Activity;)Z")
        if start != -1:
            nextm = c.find("\n.method ", start + 10)
            if nextm == -1: nextm = len(c)
            end = c.rfind(".end method", start, nextm)
            new = """.method public static require(Landroid/app/Activity;)Z
    .registers 1
    const/4 v0, 0x1
    return v0
.end method
"""
            c = c[:start] + new + c[end + len(".end method"):]
        with open(p, "w") as f:
            f.write(c)
        print("[OK] ProtectedApplication", p)

# ===== 3. TicketVerifier.verify -> always success, long time =====
for pattern in ["green/smali/**/TicketVerifier.smali", "green/smali_classes*/**/TicketVerifier.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f:
            c = f.read()
        start = c.find(".method public static verify(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;J)J")
        if start == -1:
            # try without public
            start = c.find(".method static verify(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;J)J")
        if start != -1:
            nextm = c.find("\n.method ", start + 10)
            if nextm == -1: nextm = len(c)
            end = c.rfind(".end method", start, nextm)
            # return ~1 year in ms remaining
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
            c = c[:start] + new + c[end + len(".end method"):]
            with open(p, "w") as f:
                f.write(c)
            print("[OK] TicketVerifier", p)

# ===== 4. LoginActivity - accept key \"1\" and skip web validation =====
# Make login() directly grant without network
for pattern in ["green/smali/**/LoginActivity.smali", "green/smali_classes*/**/LoginActivity.smali"]:
    for p in glob.glob(pattern, recursive=True):
        with open(p) as f:
            c = f.read()
        # relax regex so \"1\" or any short key works - replace the matches check
        # original: matches("(TNT[0-9]{6}|TNT-[A-F0-9]{32})")
        # we will make login always proceed and call Gate.grant with long time

        # Find the login method and replace body to force grant
        start = c.find(".method private login()V")
        if start == -1:
            start = c.find(".method private login()V")
        if start != -1:
            nextm = c.find("\n.method ", start + 10)
            if nextm == -1: nextm = len(c)
            end = c.rfind(".end method", start, nextm)
            # Simple force: set status, call Gate.grant with long remaining, open MainActivity
            new = """.method private login()V
    .registers 8

    # force accept any key including \"1\"
    const-wide v0, 0x757B12C00L
    const-wide v2, 0x0L

    # Gate.grant(this, remaining, expires)
    invoke-static {p0, v0, v1, v2, v3}, Lcom/zyon/jetkey/Gate;->grant(Landroid/content/Context;JJ)V

    # start MainActivity
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
.end method
"""
            c = c[:start] + new + c[end + len(".end method"):]
            with open(p, "w") as f:
                f.write(c)
            print("[OK] LoginActivity.login forced", p)

print("[*] All patches applied")
