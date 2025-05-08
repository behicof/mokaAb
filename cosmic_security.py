import hashlib
import os
import json
import time
import random
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from datetime import datetime, timedelta

class CosmicSecuritySystem:
    """
    سیستم امنیتی مکعب کیهانی:
    سامانه چندلایه برای محافظت از دانش بنیادین و تضمین دسترسی مجاز
    """
    
    def __init__(self, founder_username, foundation_date):
        self.founder_username = founder_username
        self.foundation_date = foundation_date
        self.security_initialization_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # مسیرهای امنیتی
        self.security_path = "cosmic_security"
        self.ensure_security_directories()
        
        # لایه‌های امنیتی
        self.security_layers = {
            "consciousness": self.initialize_layer("consciousness", "آگاهی", 9),
            "frequency": self.initialize_layer("frequency", "فرکانس", 7),
            "temporal": self.initialize_layer("temporal", "زمان", 5),
            "spatial": self.initialize_layer("spatial", "فضا", 6),
            "energetic": self.initialize_layer("energetic", "انرژی", 8),
            "informational": self.initialize_layer("informational", "اطلاعات", 9),
            "intentional": self.initialize_layer("intentional", "نیت", 7)
        }
        
        # تولید کلیدهای رمزنگاری
        self.encryption_keys = self.generate_encryption_keys()
        
        # ایجاد رمزهای امنیتی بنیادین
        self.foundational_passwords = self.generate_foundational_passwords()
        
        # پروتکل‌های امنیتی
        self.security_protocols = self.initialize_security_protocols()
        
        # بازیابی اضطراری
        self.emergency_recovery = self.create_emergency_recovery()
        
        # ثبت مسئول‌های مجاز (ابتدا فقط بنیان‌گذار)
        self.authorized_guardians = [{
            "username": self.founder_username,
            "role": "Founder",
            "authorization_level": 9,
            "key_fragments": 7,
            "biometric_hash": self.generate_biometric_hash(self.founder_username),
            "consciousness_signature": self.generate_consciousness_signature()
        }]
        
        # محافظ‌های زمانی
        self.temporal_guardians = self.initialize_temporal_guardians()
        
        # ذخیره اطلاعات امنیتی
        self.save_security_configuration()
        
        print(f"سیستم امنیتی مکعب کیهانی با موفقیت راه‌اندازی شد.")
        print(f"بنیان‌گذار: {self.founder_username}")
        print(f"تاریخ پایه‌گذاری: {self.foundation_date}")
        print(f"تاریخ راه‌اندازی امنیت: {self.security_initialization_date}")
    
    def ensure_security_directories(self):
        """ایجاد ساختار دایرکتوری امنیتی"""
        directories = [
            self.security_path,
            os.path.join(self.security_path, "keys"),
            os.path.join(self.security_path, "logs"),
            os.path.join(self.security_path, "backups"),
            os.path.join(self.security_path, "protocols"),
            os.path.join(self.security_path, "recovery"),
            os.path.join(self.security_path, "guardians")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def initialize_layer(self, code_name, persian_name, security_level):
        """راه‌اندازی یک لایه امنیتی"""
        return {
            "name": code_name,
            "persian_name": persian_name,
            "level": security_level,
            "activation_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "frequency": self.calculate_security_frequency(code_name),
            "checksum": self.generate_layer_checksum(code_name, security_level),
            "access_code": self.generate_layer_access_code(code_name),
            "guardian_key": self.generate_guardian_key(code_name, security_level)
        }
    
    def calculate_security_frequency(self, layer_name):
        """محاسبه فرکانس امنیتی بر اساس نام لایه"""
        base_frequencies = {
            "consciousness": 963.0,
            "frequency": 417.0,
            "temporal": 741.0,
            "spatial": 528.0,
            "energetic": 852.0,
            "informational": 396.0,
            "intentional": 639.0
        }
        
        if layer_name in base_frequencies:
            # اضافه کردن مقدار کوچک و منحصر به فرد بر اساس تاریخ
            day_offset = int(self.foundation_date.split("-")[2].split(" ")[0]) * 0.01
            return base_frequencies[layer_name] + day_offset
        
        # فرکانس پیش‌فرض
        return 432.0
    
    def generate_layer_checksum(self, layer_name, security_level):
        """تولید چک‌سام امنیتی برای لایه"""
        data = f"{layer_name}-{security_level}-{self.founder_username}-{self.foundation_date}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def generate_layer_access_code(self, layer_name):
        """تولید کد دسترسی برای لایه"""
        seed = f"{layer_name}-{self.founder_username}-{int(time.time())}"
        hash_val = hashlib.sha512(seed.encode()).hexdigest()
        # گرفتن ۱۲ کاراکتر از هش به عنوان کد دسترسی
        return f"COSMIC-{layer_name.upper()}-{hash_val[:12].upper()}"
    
    def generate_guardian_key(self, layer_name, security_level):
        """تولید کلید محافظ برای لایه"""
        key_material = f"{layer_name}-{security_level}-{self.founder_username}-{int(time.time())}"
        return hashlib.sha384(key_material.encode()).hexdigest()
    
    def generate_encryption_keys(self):
        """تولید کلیدهای رمزنگاری"""
        keys = {}
        
        # برای هر لایه یک کلید رمزنگاری تولید می‌کنیم
        for layer_name in self.security_layers:
            # تولید کلید Fernet
            password = f"{layer_name}-{self.founder_username}-{self.foundation_date}".encode()
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            
            keys[layer_name] = {
                "key": key.decode(),
                "salt": base64.b64encode(salt).decode(),
                "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "key_id": f"KEY-{layer_name.upper()}-{int(time.time())}"
            }
            
            # ذخیره کلید در فایل جداگانه
            key_path = os.path.join(self.security_path, "keys", f"{layer_name}_key.json")
            with open(key_path, 'w') as f:
                # نکته امنیتی: در یک سیستم واقعی، کلیدها نباید به صورت متن ساده ذخیره شوند
                json.dump(keys[layer_name], f, indent=2)
        
        # کلید اصلی سیستم
        master_password = f"MASTER-{self.founder_username}-{self.foundation_date}-COSMIC-CUBE".encode()
        master_salt = os.urandom(16)
        master_kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=master_salt,
            iterations=150000,
        )
        master_key = base64.urlsafe_b64encode(master_kdf.derive(master_password))
        
        keys["master"] = {
            "key": master_key.decode(),
            "salt": base64.b64encode(master_salt).decode(),
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "key_id": f"MASTER-KEY-{int(time.time())}"
        }
        
        master_key_path = os.path.join(self.security_path, "keys", "master_key.json")
        with open(master_key_path, 'w') as f:
            json.dump(keys["master"], f, indent=2)
        
        return keys
    
    def generate_foundational_passwords(self):
        """تولید رمزهای بنیادین برای دسترسی بحرانی"""
        passwords = {}
        
        # یک رمز اصلی بنیادین
        foundation_seed = f"{self.founder_username}-{self.foundation_date}-COSMIC-FOUNDATION"
        foundation_hash = hashlib.sha512(foundation_seed.encode()).hexdigest()
        
        # رمز اصلی: ترکیبی از حروف و اعداد و نمادها
        master_pwd = foundation_hash[:8].upper() + "-" + foundation_hash[8:16] + "-" + foundation_hash[16:24].upper()
        
        passwords["master"] = {
            "password": master_pwd,
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "expiration_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "hash": hashlib.sha256(master_pwd.encode()).hexdigest()
        }
        
        # رمزهای لایه‌ای
        for layer_name in self.security_layers:
            layer_seed = f"{layer_name}-{self.founder_username}-{self.foundation_date}-{int(time.time())}"
            layer_hash = hashlib.sha512(layer_seed.encode()).hexdigest()
            
            # رمز لایه: ترکیبی منحصر به فرد
            layer_pwd = layer_hash[:6].upper() + "-" + layer_hash[6:12] + "-" + layer_hash[12:18].upper()
            
            passwords[layer_name] = {
                "password": layer_pwd,
                "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "expiration_date": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"),
                "hash": hashlib.sha256(layer_pwd.encode()).hexdigest()
            }
        
        # رمز بازیابی اضطراری
        emergency_seed = f"EMERGENCY-{self.founder_username}-{self.foundation_date}-{int(time.time())}"
        emergency_hash = hashlib.sha512(emergency_seed.encode()).hexdigest()
        
        # رمز اضطراری: ساختار خاص
        emergency_pwd = "EM-" + emergency_hash[:4].upper() + "-" + emergency_hash[4:12] + "-" + emergency_hash[12:16].upper() + "-RESTORE"
        
        passwords["emergency"] = {
            "password": emergency_pwd,
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "expiration_date": (datetime.now() + timedelta(days=1825)).strftime("%Y-%m-%d"),  # 5 سال
            "hash": hashlib.sha256(emergency_pwd.encode()).hexdigest()
        }
        
        # ذخیره هش‌های رمزها (نه خود رمزها)
        password_hashes = {k: {"hash": v["hash"], "creation_date": v["creation_date"], "expiration_date": v["expiration_date"]} for k, v in passwords.items()}
        
        hashes_path = os.path.join(self.security_path, "keys", "password_hashes.json")
        with open(hashes_path, 'w') as f:
            json.dump(password_hashes, f, indent=2)
        
        return passwords
    
    def initialize_security_protocols(self):
        """راه‌اندازی پروتکل‌های امنیتی"""
        protocols = {
            "authentication": {
                "name": "COSMIC-AUTH",
                "levels": 7,
                "frequency_verification": True,
                "consciousness_check": True,
                "timeline_verification": True,
                "methods": ["password", "key", "frequency", "consciousness", "intent", "biometric", "temporal"],
                "required_methods": 3,  # حداقل سه روش برای احراز هویت نیاز است
                "timeout": 300,  # تایم‌اوت ۵ دقیقه
                "lockout_threshold": 5,  # قفل پس از ۵ تلاش ناموفق
                "recovery_period": 3600  # دوره بازیابی ۱ ساعت
            },
            "encryption": {
                "name": "COSMIC-CRYPT",
                "algorithms": ["AES-256", "quantum-resistant-lattice", "frequency-encoded"],
                "key_rotation": 180,  # چرخش کلید هر ۱۸۰ روز
                "multi_layer": True
            },
            "backup": {
                "name": "COSMIC-BACKUP",
                "frequency": 24,  # بک‌آپ هر ۲۴ ساعت
                "retention": 7,  # نگهداری ۷ نسخه
                "locations": 3,  # ذخیره در ۳ مکان مختلف
                "encryption": True,
                "quantum_encoding": True,
                "consciousness_imprint": True
            },
            "access_control": {
                "name": "COSMIC-ACCESS",
                "roles": ["Founder", "Guardian", "Keeper", "Seeker", "Student"],
                "domain_separation": True,
                "least_privilege": True,
                "need_to_know": True,
                "approval_required": True
            },
            "intrusion_detection": {
                "name": "COSMIC-SENTINEL",
                "monitoring": True,
                "consciousness_alerts": True,
                "frequency_monitoring": True,
                "timeline_alerts": True,
                "quantum_detection": True
            },
            "temporal_protection": {
                "name": "COSMIC-TIMELINE",
                "timeline_anchoring": True,
                "continuum_verification": True,
                "reality_checkpoints": 7,
                "quantum_entanglement": True,
                "past_protection": True,
                "future_projection": True
            },
            "emergency_protocol": {
                "name": "COSMIC-PRESERVE",
                "activation_methods": 3,
                "guardian_consensus": True,
                "automatic_sealing": True,
                "knowledge_preservation": True,
                "dimensional_shift": True
            }
        }
        
        # ذخیره پروتکل‌ها
        for protocol_name, protocol in protocols.items():
            protocol_path = os.path.join(self.security_path, "protocols", f"{protocol_name}.json")
            with open(protocol_path, 'w') as f:
                json.dump(protocol, f, indent=2)
        
        return protocols
    
    def create_emergency_recovery(self):
        """ایجاد سیستم بازیابی اضطراری"""
        recovery = {
            "activation_code": self.generate_emergency_code(),
            "key_fragments": 7,  # کلید به ۷ بخش تقسیم می‌شود
            "threshold": 4,  # دست‌کم ۴ بخش برای بازیابی نیاز است
            "guardian_approval": 2,  # تأیید حداقل ۲ محافظ
            "founder_override": True,  # بنیان‌گذار می‌تواند بدون محدودیت بازیابی کند
            "cosmic_synchronization": True,  # همگام‌سازی با الگوهای کیهانی
            "recovery_windows": [  # بازه‌های زمانی بازیابی
                {"start": "03:00", "end": "04:00", "days": ["Monday", "Thursday"]},
                {"start": "15:00", "end": "16:00", "days": ["Tuesday", "Friday"]},
                {"start": "21:00", "end": "22:00", "days": ["Wednesday", "Sunday"]}
            ],
            "frequency_keys": self.generate_frequency_keys(),
            "recovery_procedures": [
                "1. احراز هویت چندلایه",
                "2. تأیید با کد اضطراری",
                "3. ارائه بخش‌های کلید",
                "4. همگام‌سازی فرکانسی",
                "5. تأیید آگاهی",
                "6. فعال‌سازی رابط بازیابی",
                "7. بازیابی تدریجی داده‌ها"
            ]
        }
        
        # ایجاد بخش‌های کلید بازیابی
        recovery_key = os.urandom(32).hex()
        fragments = []
        
        for i in range(recovery["key_fragments"]):
            fragment_seed = f"{recovery_key}-{i}-{self.founder_username}-{int(time.time())}"
            fragment = hashlib.sha256(fragment_seed.encode()).hexdigest()
            fragments.append({
                "index": i + 1,
                "fragment": fragment,
                "guardian": f"Guardian-{i+1}" if i > 0 else self.founder_username
            })
        
        recovery["key_fragments_data"] = fragments
        
        # ذخیره اطلاعات بازیابی
        recovery_path = os.path.join(self.security_path, "recovery", "emergency_protocol.json")
        with open(recovery_path, 'w') as f:
            json.dump(recovery, f, indent=2)
        
        return recovery
    
    def generate_emergency_code(self):
        """تولید کد اضطراری"""
        code_seed = f"EMERGENCY-{self.founder_username}-{self.foundation_date}-{int(time.time() * 1000)}"
        code_hash = hashlib.sha512(code_seed.encode()).hexdigest()
        
        # ساختار کد: COSMIC-EM-XXXX-YYYY-ZZZZ
        return f"COSMIC-EM-{code_hash[:4].upper()}-{code_hash[4:8].upper()}-{code_hash[8:12].upper()}"
    
    def generate_frequency_keys(self):
        """تولید کلیدهای فرکانسی برای بازیابی"""
        frequencies = {
            "432Hz": "وحدت کیهانی",
            "528Hz": "ترمیم و بازیابی",
            "963Hz": "ارتباط با آگاهی برتر",
            "741Hz": "حل مشکلات",
            "852Hz": "روشن بینی درونی",
            "396Hz": "رهایی از ترس",
            "639Hz": "ارتباط و هماهنگی"
        }
        
        return frequencies
    
    def generate_biometric_hash(self, username):
        """شبیه‌سازی تولید هش بیومتریک"""
        # در سیستم واقعی، این از اسکن بیومتریک واقعی تولید می‌شود
        seed = f"{username}-BIOMETRIC-{self.foundation_date}-{int(time.time())}"
        return hashlib.sha512(seed.encode()).hexdigest()
    
    def generate_consciousness_signature(self):
        """تولید امضای آگاهی"""
        # در سیستم واقعی، این از الگوهای امواج مغزی و میدان‌های انرژی کاربر تولید می‌شود
        components = []
        
        # شبیه‌سازی الگوهای مختلف امواج مغزی و انرژی
        for i in range(7):
            component_seed = f"CONSCIOUSNESS-{i}-{self.founder_username}-{int(time.time())}"
            component = hashlib.sha256(component_seed.encode()).hexdigest()
            components.append(component)
        
        # ترکیب اجزا
        signature = "-".join([comp[:8] for comp in components])
        
        return signature
    
    def initialize_temporal_guardians(self):
        """تنظیم محافظ‌های زمانی"""
        guardians = []
        
        # ایجاد محافظ‌ها برای بازه‌های زمانی مختلف
        time_periods = [
            {"name": "گذشته نزدیک", "start_year": 2020, "end_year": 2024},
            {"name": "زمان حال", "start_year": 2025, "end_year": 2030},
            {"name": "آینده نزدیک", "start_year": 2031, "end_year": 2050},
            {"name": "آینده میانی", "start_year": 2051, "end_year": 2100},
            {"name": "آینده دور", "start_year": 2101, "end_year": 2200}
        ]
        
        for period in time_periods:
            guardian_seed = f"GUARDIAN-{period['name']}-{self.founder_username}-{int(time.time())}"
            guardian_hash = hashlib.sha512(guardian_seed.encode()).hexdigest()
            
            guardian = {
                "period": period,
                "key": guardian_hash,
                "activation_frequency": self.calculate_temporal_frequency(period),
                "synchronization_code": self.generate_temporal_sync_code(period),
                "access_protocol": "TEMPORAL-SYNC-" + guardian_hash[:12].upper()
            }
            
            guardians.append(guardian)
        
        # ذخیره اطلاعات محافظان زمانی
        guardians_path = os.path.join(self.security_path, "guardians", "temporal_guardians.json")
        with open(guardians_path, 'w') as f:
            json.dump(guardians, f, indent=2)
        
        return guardians
    
    def calculate_temporal_frequency(self, period):
        """محاسبه فرکانس زمانی برای هر دوره"""
        # هر دوره زمانی فرکانس خاص خود را دارد
        base_frequency = 432.0
        
        # نگاشت غیرخطی سال‌ها به فرکانس
        year_span = period["end_year"] - period["start_year"]
        year_factor = 1 + (period["start_year"] - 2000) / 1000
        
        return round(base_frequency * year_factor + year_span * 0.01, 2)
    
    def generate_temporal_sync_code(self, period):
        """تولید کد همگام‌سازی زمانی"""
        code_seed = f"SYNC-{period['name']}-{period['start_year']}-{period['end_year']}-{int(time.time())}"
        code_hash = hashlib.sha384(code_seed.encode()).hexdigest()
        
        # ساختار کد: TEMPORAL-[دوره زمانی]-XXXX-YYYY
        period_code = period["name"].upper().replace(" ", "-")
        return f"TEMPORAL-{period_code}-{code_hash[:4].upper()}-{code_hash[4:8].upper()}"
    
    def save_security_configuration(self):
        """ذخیره پیکربندی امنیتی پایه"""
        # اطلاعات عمومی امنیتی - بدون رمزهای محرمانه
        public_config = {
            "founder": self.founder_username,
            "foundation_date": self.foundation_date,
            "security_initialization_date": self.security_initialization_date,
            "security_layers": {name: self.get_public_layer_info(layer) for name, layer in self.security_layers.items()},
            "security_protocols": {name: protocol["name"] for name, protocol in self.security_protocols.items()},
            "authorized_guardians_count": len(self.authorized_guardians),
            "temporal_guardians_count": len(self.temporal_guardians),
            "emergency_recovery_enabled": True,
            "version": "1.0.0",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # ذخیره پیکربندی عمومی
        config_path = os.path.join(self.security_path, "security_configuration.json")
        with open(config_path, 'w') as f:
            json.dump(public_config, f, indent=2)
    
    def get_public_layer_info(self, layer):
        """گرفتن اطلاعات عمومی لایه امنیتی - بدون اطلاعات حساس"""
        return {
            "name": layer["name"],
            "persian_name": layer["persian_name"],
            "level": layer["level"],
            "activation_timestamp": layer["activation_timestamp"],
            "frequency": layer["frequency"]
        }
    
    def encrypt_data(self, data, layer_name="master"):
        """رمزنگاری داده‌ها با کلید لایه مشخص شده"""
        if layer_name not in self.encryption_keys:
            raise ValueError(f"کلید رمزنگاری برای لایه {layer_name} یافت نشد.")
        
        # ایجاد رمزکننده Fernet با کلید لایه
        key = self.encryption_keys[layer_name]["key"]
        cipher = Fernet(key.encode())
        
        # تبدیل داده به رشته JSON و رمزنگاری
        if isinstance(data, (dict, list)):
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        elif isinstance(data, str):
            data = data.encode('utf-8')
        
        encrypted_data = cipher.encrypt(data)
        
        # افزودن اطلاعات رمزنگاری
        result = {
            "encrypted_data": base64.b64encode(encrypted_data).decode('utf-8'),
            "encryption_method": "Fernet",
            "layer": layer_name,
            "key_id": self.encryption_keys[layer_name]["key_id"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return result
    
    def decrypt_data(self, encrypted_package, layer_name=None):
        """رمزگشایی داده‌ها"""
        # تعیین لایه از بسته رمزنگاری اگر مشخص نشده
        if layer_name is None and "layer" in encrypted_package:
            layer_name = encrypted_package["layer"]
            
        if layer_name not in self.encryption_keys:
            raise ValueError(f"کلید رمزگشایی برای لایه {layer_name} یافت نشد.")
        
        # ایجاد رمزگشا با کلید لایه
        key = self.encryption_keys[layer_name]["key"]
        cipher = Fernet(key.encode())
        
        # رمزگشایی داده‌ها
        encrypted_data = base64.b64decode(encrypted_package["encrypted_data"])
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # تلاش برای تبدیل به JSON
        try:
            return json.loads(decrypted_data)
        except json.JSONDecodeError:
            # اگر JSON نیست، به صورت رشته برگردان
            return decrypted_data.decode('utf-8')
        
    def verify_authentication(self, username, password, additional_factors=None):
        """بررسی احراز هویت چندعاملی"""
        # شبیه‌سازی بررسی احراز هویت
        
        # بررسی کاربر مجاز
        authorized_user = next((user for user in self.authorized_guardians if user["username"] == username), None)
        if not authorized_user:
            return {"success": False, "message": "کاربر مجاز نیست."}
        
        # بررسی رمز عبور
        # در سیستم واقعی، رمز عبور هش شده مقایسه می‌شود
        master_hash = self.foundational_passwords["master"]["hash"]
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if input_hash != master_hash:
            return {"success": False, "message": "رمز عبور نادرست است."}
        
        # بررسی عوامل دیگر (فرکانس، آگاهی و غیره)
        required_factors = self.security_protocols["authentication"]["required_methods"]
        authentication_level = 1  # رمز عبور تأیید شده
        
        if additional_factors:
            # شبیه‌سازی بررسی عوامل اضافی
            if "frequency" in additional_factors:
                authentication_level += 1
            if "consciousness" in additional_factors:
                authentication_level += 1
            if "biometric" in additional_factors:
                authentication_level += 1
            if "intent" in additional_factors:
                authentication_level += 1
        
        if authentication_level < required_factors:
            return {
                "success": False, 
                "message": f"حداقل {required_factors} عامل احراز هویت نیاز است. {authentication_level} عامل تأیید شد."
            }
        
        # احراز هویت موفق
        return {
            "success": True,
            "username": username,
            "authentication_level": authentication_level,
            "session_expiry": (datetime.now() + timedelta(minutes=self.security_protocols["authentication"]["timeout"])).strftime("%Y-%m-%d %H:%M:%S"),
            "access_level": authorized_user["authorization_level"]
        }
    
    def backup_knowledge(self, knowledge_nodes):
        """تهیه نسخه پشتیبان از گره‌های دانش"""
        # تعیین مکان پشتیبان‌گیری
        backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(self.security_path, "backups", backup_time)
        os.makedirs(backup_folder, exist_ok=True)
        
        # رمزنگاری و ذخیره هر گره
        for i, node in enumerate(knowledge_nodes):
            # انتخاب لایه رمزنگاری بر اساس بُعد گره
            layer_name = node.get("dimension", "information")
            if layer_name not in self.encryption_keys:
                layer_name = "master"  # استفاده از کلید اصلی اگر لایه مناسب یافت نشد
            
            # رمزنگاری گره
            encrypted_node = self.encrypt_data(node, layer_name)
            
            # ذخیره در فایل
            node_filename = f"node_{i+1}_{node.get('id', str(i))}.enc"
            node_path = os.path.join(backup_folder, node_filename)
            
            with open(node_path, 'w') as f:
                json.dump(encrypted_node, f, indent=2)
        
        # ایجاد فایل فهرست
        manifest = {
            "backup_time": backup_time,
            "founder": self.founder_username,
            "node_count": len(knowledge_nodes),
            "encryption_layers_used": list(set(node.get("dimension", "information") for node in knowledge_nodes)),
            "checksum": self.generate_backup_checksum(knowledge_nodes)
        }
        
        manifest_path = os.path.join(backup_folder, "manifest.json")
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return {
            "success": True,
            "backup_location": backup_folder,
            "backup_time": backup_time,
            "node_count": len(knowledge_nodes)
        }
    
    def generate_backup_checksum(self, knowledge_nodes):
        """تولید چک‌سام برای بررسی صحت نسخه پشتیبان"""
        # ترکیب تمام داده‌ها و تولید هش
        combined_data = json.dumps(knowledge_nodes, sort_keys=True).encode('utf-8')
        return hashlib.sha256(combined_data).hexdigest()
    
    def restore_knowledge(self, backup_time, authentication_result):
        """بازیابی دانش از نسخه پشتیبان"""
        # بررسی مجاز بودن کاربر
        if not authentication_result["success"]:
            return {"success": False, "message": "احراز هویت معتبر نیست."}
        
        if authentication_result["access_level"] < 7:
            return {"success": False, "message": "سطح دسترسی کافی برای بازیابی نیست."}
        
        # بررسی وجود نسخه پشتیبان
        backup_folder = os.path.join(self.security_path, "backups", backup_time)
        if not os.path.exists(backup_folder):
            return {"success": False, "message": "نسخه پشتیبان یافت نشد."}
        
        # بررسی وجود فایل فهرست
        manifest_path = os.path.join(backup_folder, "manifest.json")
        if not os.path.exists(manifest_path):
            return {"success": False, "message": "فایل فهرست نسخه پشتیبان یافت نشد."}
        
        # بارگیری فهرست
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        # بازیابی گره‌ها
        restored_nodes = []
        for i in range(1, manifest["node_count"] + 1):
            # جستجوی فایل گره
            node_files = [f for f in os.listdir(backup_folder) if f.startswith(f"node_{i}_")]
            
            if not node_files:
                continue
                
            node_path = os.path.join(backup_folder, node_files[0])
            
            # بارگیری گره رمزنگاری شده
            with open(node_path, 'r') as f:
                encrypted_node = json.load(f)
            
            # رمزگشایی گره
            try:
                node = self.decrypt_data(encrypted_node)
                restored_nodes.append(node)
            except Exception as e:
                print(f"خطا در رمزگشایی گره {i}: {e}")
        
        # بررسی صحت بازیابی
        if len(restored_nodes) != manifest["node_count"]:
            return {
                "success": False, 
                "message": f"بازیابی ناقص. {len(restored_nodes)} از {manifest['node_count']} گره بازیابی شد."
            }
        
        return {
            "success": True,
            "message": f"{len(restored_nodes)} گره دانش با موفقیت بازیابی شد.",
            "restored_nodes": restored_nodes
        }