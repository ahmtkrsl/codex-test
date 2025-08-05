# Pomodoro Timer

Bu depo, Pomodoro tekniğini takip eden basit bir Python zamanlayıcısı içerir.
Zamanlayıcı otomatik veya manuel geçişlerle çalışma, kısa mola ve uzun mola
oturumları arasında döngü yapabilir.

## Çalıştırma

```bash
python -m pomodoro.cli
```

Varsayılan değerler 25/5/15 dakikadır. Süreleri ve döngü sayısını ayarlamak
 için `--work`, `--short`, `--long`, `--cycles` bayraklarını kullanın. Manuel geçiş
 için `--manual` bayrağını ekleyin.

## Testler

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Ünite testleri zamanlayıcı mantığının doğru çalıştığını doğrular.
