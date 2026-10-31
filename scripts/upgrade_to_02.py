from pathlib import Path
p=Path("app/src/main/java/ua/fat32formatter/MainActivity.java")
s=p.read_text()
s=s.replace("import android.graphics.Color;", "import android.graphics.Color;\nimport android.animation.ObjectAnimator;\nimport android.animation.AnimatorSet;\nimport android.widget.FrameLayout;\nimport java.util.Arrays;")
s=s.replace("private Fat32Layout prepared;", "private Fat32Layout prepared;\n    private byte[] originalSectorZero;")
s=s.replace("        scanDevices();\n    }", "        scanDevices();\n        showLaunchAnimation();\n    }", 1)
s=s.replace('addText(root, "◈ USB FAT32", 29, ACCENT, true);','addText(root, "FAT32 Майстер", 29, ACCENT, true);')
s=s.replace("        selected = null; prepared = null;", "        selected = null; prepared = null; originalSectorZero = null;")
s=s.replace("        selected = d; prepared = null;", "        selected = d; prepared = null; originalSectorZero = null;")
s=s.replace("                Fat32Layout layout = Fat32Layout.create(disk.blockCount());\n                runOnUiThread(() -> {", "                Fat32Layout layout = Fat32Layout.create(disk.blockCount());\n                byte[] sectorZero = new byte[512];\n                disk.read(0, sectorZero);\n                runOnUiThread(() -> {")
s=s.replace("                    prepared = layout;\n", "                    prepared = layout;\n                    originalSectorZero = sectorZero;\n")
s=s.replace('status.setText("Сумісність перевірено. Можна форматувати.");', 'status.setText("USB прочитано. Запис ще не перевірено на цій флешці.");')
s=s.replace('final Fat32Layout layout = prepared;', 'final Fat32Layout layout = prepared;\n        final byte[] expectedSector = originalSectorZero == null ? null : originalSectorZero.clone();')
s=s.replace('typeToConfirm(d, layout)', 'typeToConfirm(d, layout, expectedSector)')
s=s.replace('private void typeToConfirm(UsbDevice d, Fat32Layout layout)', 'private void typeToConfirm(UsbDevice d, Fat32Layout layout, byte[] expectedSector)')
s=s.replace('doFormat(d, layout);', 'doFormat(d, layout, expectedSector);')
s=s.replace('private void doFormat(UsbDevice d, Fat32Layout layout)', 'private void doFormat(UsbDevice d, Fat32Layout layout, byte[] expectedSector)')
s=s.replace('            try (UsbBotBlockDevice disk = new UsbBotBlockDevice(manager, d)) {\n                Fat32Formatter.format(disk, layout,', '            try (UsbBotBlockDevice disk = new UsbBotBlockDevice(manager, d)) {\n                if (expectedSector == null) throw new java.io.IOException("Не виконано попередню перевірку USB.");\n                byte[] actual = new byte[512];\n                disk.read(0, actual);\n                if (!Arrays.equals(expectedSector, actual)) throw new java.io.IOException("Флешка змінилася після перевірки. Запис скасовано.");\n                Fat32Formatter.format(disk, layout,')
s=s.replace('b.setText(text); b.setTextAllCaps(false);', 'b.setText(text);')
s=s.replace("    private void scanDevices() {", '''    private void showLaunchAnimation() {
        FrameLayout host = findViewById(android.R.id.content);
        FrameLayout overlay = new FrameLayout(this);
        overlay.setBackgroundColor(BG);
        host.addView(overlay, new FrameLayout.LayoutParams(-1, -1));
        LinearLayout brand = new LinearLayout(this);
        brand.setOrientation(LinearLayout.VERTICAL);
        brand.setGravity(Gravity.CENTER);
        overlay.addView(brand, new FrameLayout.LayoutParams(-1, -1));
        TextView symbol = addText(brand, "◆", 72, ACCENT, true);
        symbol.setGravity(Gravity.CENTER);
        TextView name = addText(brand, "FAT32 Майстер", 29, TEXT, true);
        name.setGravity(Gravity.CENTER);
        TextView subtitle = addText(brand, "USB OTG • FAT32", 15, MUTED, false);
        subtitle.setGravity(Gravity.CENTER);
        AnimatorSet pulse = new AnimatorSet();
        pulse.playTogether(
            ObjectAnimator.ofFloat(symbol, "scaleX", 0.7f, 1.14f, 1f),
            ObjectAnimator.ofFloat(symbol, "scaleY", 0.7f, 1.14f, 1f));
        pulse.setDuration(750);
        pulse.start();
        overlay.animate().alpha(0f).setStartDelay(1100).setDuration(300)
              .withEndAction(() -> host.removeView(overlay)).start();
    }

    private void scanDevices() {''',1)
p.write_text(s)
q=Path("app/src/main/java/ua/fat32formatter/UsbBotBlockDevice.java")
s=q.read_text().replace("opened.claimInterface(chosen, true)", "opened.claimInterface(chosen, false)")
q.write_text(s)
q=Path("app/src/main/AndroidManifest.xml")
s=q.read_text().replace('android:label="USB FAT32 Formatter"', 'android:label="FAT32 Майстер" android:icon="@android:drawable/ic_menu_save"')
q.write_text(s)
q=Path("app/build.gradle")
s=q.read_text().replace("versionCode 1","versionCode 2").replace("versionName '0.1.0-beta'","versionName '0.2.0-beta'")
q.write_text(s)
print("Applied FAT32 Майстер branding, splash and read-before-write checks")
