# 학생용 Quick Commands

## Windows PowerShell

```powershell
wsl -l -v
wsl -d Ubuntu-22.04
```

## Ubuntu

```bash
lsb_release -a
uname -m
free -h
df -h /
ip addr
ping -c 4 127.0.0.1
```

## Terminal 1 — Server

```bash
mkdir -p ~/network_lab
cd ~/network_lab
echo "ROBOT NETWORK OK" > index.html
python3 -m http.server 8000
```

## Terminal 2 — Client

```bash
curl http://127.0.0.1:8000
```

## 장애 주입

```bash
curl http://127.0.0.1:9000
```

## 재검증

```bash
curl http://127.0.0.1:8000
```
