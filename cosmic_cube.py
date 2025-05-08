import pygame
import numpy as np
import json
import os
import time
import math
import random
from datetime import datetime
import pygame.gfxdraw
from scipy.spatial.transform import Rotation
from pygame.locals import *

class CosmicCube:
    """
    مکعب کیهانی: سیستم پایه‌گذاری و یکپارچه‌سازی دانش کیهانی
    یک سیستم چندبُعدی برای تجسم، کاوش و دستکاری دانش کیهانی
    """
    
    def __init__(self, username="behicof", timestamp=None):
        # اطلاعات پایه
        self.username = username
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.foundation_date = "2025-04-17 14:37:51"
        self.version = "1.0.0"
        
        # مسیرها و داده‌ها
        self.data_path = "cosmic_foundations"
        self.ensure_directories()
        
        # ابعاد کیهانی
        self.dimensions = {
            "consciousness": 0.0,  # آگاهی
            "frequency": 0.0,      # فرکانس
            "time": 0.0,          # زمان
            "space": 0.0,         # فضا
            "energy": 0.0,        # انرژی
            "information": 0.0,   # اطلاعات
            "intention": 0.0      # نیت
        }
        
        # سیستم‌های اصلی
        self.systems = {
            "knowledge_core": {"active": True, "level": 1},
            "reality_matrix": {"active": True, "level": 1},
            "timeline_navigator": {"active": True, "level": 1},
            "consciousness_amplifier": {"active": True, "level": 1},
            "holographic_projector": {"active": True, "level": 1},
            "quantum_resonator": {"active": True, "level": 1}
        }
        
        # مفاهیم بنیادی کیهانی
        self.core_concepts = self.load_core_concepts()
        
        # روابط کیهانی
        self.cosmic_relationships = []
        
        # هسته دانش
        self.knowledge_nodes = []
        
        # تاریخچه کاوش
        self.exploration_history = []
        
        # وضعیت فعلی
        self.current_state = {
            "mode": "foundation",
            "focus": None,
            "active_dimension": None,
            "vibration": 7.83,  # فرکانس شومان زمین به عنوان پایه
            "stability": 1.0
        }
        
        # شبکه ارتباطی
        self.connection_network = {}
        
        # شروع سیستم تجسم
        self.init_visualization()
        
        # تولید دانش اولیه
        self.generate_foundation_knowledge()

    def ensure_directories(self):
        """ایجاد ساختار دایرکتوری پایه‌گذاری"""
        directories = [
            self.data_path,
            os.path.join(self.data_path, "core_concepts"),
            os.path.join(self.data_path, "knowledge_nodes"),
            os.path.join(self.data_path, "reality_matrices"),
            os.path.join(self.data_path, "timelines"),
            os.path.join(self.data_path, "frequency_patterns"),
            os.path.join(self.data_path, "consciousness_maps")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def load_core_concepts(self):
        """بارگیری مفاهیم بنیادی کیهانی"""
        try:
            concept_path = os.path.join(self.data_path, "core_concepts", "fundamental.json")
            if os.path.exists(concept_path):
                with open(concept_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading core concepts: {e}")
        
        # مفاهیم پایه پیش‌فرض
        return {
            "unity": {
                "name": "وحدت کیهانی",
                "description": "اصل بنیادی اتصال همه چیز در یک میدان آگاهی یکپارچه",
                "frequency": 432.0,
                "symbols": ["⊕", "☯", "⊗"],
                "related_concepts": ["oneness", "interconnection", "wholeness"]
            },
            "duality": {
                "name": "دوگانگی خلاق",
                "description": "اصل تضاد و تکمیل که موجب خلق واقعیت می‌شود",
                "frequency": 144.0,
                "symbols": ["☯", "⊖", "⊙"],
                "related_concepts": ["polarity", "balance", "dynamics"]
            },
            "harmony": {
                "name": "هماهنگی کیهانی",
                "description": "اصل سازماندهی الگوهای فرکانسی در وضعیت تعادل",
                "frequency": 528.0,
                "symbols": ["∞", "♫", "⌘"],
                "related_concepts": ["resonance", "balance", "alignment"]
            },
            "consciousness": {
                "name": "آگاهی اساسی",
                "description": "ماهیت بنیادی واقعیت به عنوان میدانی از آگاهی نامحدود",
                "frequency": 963.0,
                "symbols": ["☉", "♾", "⊛"],
                "related_concepts": ["awareness", "presence", "observation"]
            },
            "creation": {
                "name": "خلقت مداوم",
                "description": "اصل خلق مداوم واقعیت از طریق آگاهی و نیت",
                "frequency": 396.0,
                "symbols": ["⚹", "⚛", "⚷"],
                "related_concepts": ["manifestation", "intention", "expression"]
            },
            "evolution": {
                "name": "تکامل کیهانی",
                "description": "اصل حرکت پیوسته به سوی پیچیدگی و آگاهی بالاتر",
                "frequency": 741.0,
                "symbols": ["↑", "⟳", "⇝"],
                "related_concepts": ["growth", "expansion", "transcendence"]
            },
            "resonance": {
                "name": "تشدید کوانتومی",
                "description": "اصل ارتباط و تأثیر متقابل از طریق هماهنگی فرکانسی",
                "frequency": 417.0,
                "symbols": ["≈", "∿", "≋"],
                "related_concepts": ["vibration", "entrainment", "sympathy"]
            }
        }
    
    def init_visualization(self):
        """آماده‌سازی سیستم تجسم"""
        pygame.init()
        self.width, self.height = 1280, 800
        self.screen = pygame.display.set_mode((self.width, self.height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("مکعب کیهانی - پایه‌گذاری دانش بنیادین")
        
        # فونت‌ها
        self.fonts = {
            "tiny": pygame.font.SysFont('Arial', 12),
            "small": pygame.font.SysFont('Arial', 16),
            "medium": pygame.font.SysFont('Arial', 24),
            "large": pygame.font.SysFont('Arial', 36),
            "huge": pygame.font.SysFont('Arial', 48)
        }
        
        # رنگ‌ها
        self.colors = {
            'background': (5, 10, 25),
            'grid': (20, 30, 50),
            'text': (220, 220, 255),
            'highlight': (100, 150, 250),
            'consciousness': (230, 100, 240),
            'frequency': (100, 200, 240),
            'time': (240, 200, 100),
            'space': (100, 240, 150),
            'energy': (240, 150, 100),
            'information': (150, 200, 240),
            'intention': (200, 150, 240),
            'unity': (255, 255, 255),
            'node_core': (150, 100, 255),
            'node_glow': (100, 150, 255, 100)
        }
        
        # المان‌های بصری
        self.stars = []
        self.energy_particles = []
        self.cube_rotation = Rotation.from_euler('xyz', [0, 0, 0])
        self.cube_vertices = np.array([
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ])
        self.cube_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
        # ایجاد ستاره‌ها و ذرات انرژی
        self.create_stars(500)
        self.create_energy_particles(100)
        
        # سیستم صفحه کلید و ماوس
        self.keys_pressed = set()
        self.mouse_pos = (0, 0)
        self.mouse_pressed = False
        
        # متغیرهای انیمیشن
        self.animation_time = 0
        self.auto_rotate = True
        self.rotation_speed = 0.005
        
        # زاویه دید و فاصله
        self.view_distance = 5.0
        self.fov = 50.0
        
        # متغیرهای رابط کاربری
        self.ui_panels = {
            "dimensions": pygame.Rect(20, 20, 200, 300),
            "systems": pygame.Rect(self.width - 220, 20, 200, 300),
            "explorer": pygame.Rect(20, self.height - 320, self.width - 40, 300)
        }
        self.ui_active_panel = None
    
    def create_stars(self, count):
        """ایجاد ستاره‌های پس‌زمینه"""
        self.stars = []
        for _ in range(count):
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            z = random.randint(-100, 100)
            size = random.uniform(0.5, 2.5)
            brightness = random.uniform(100, 255)
            self.stars.append({
                'pos': (x, y, z),
                'size': size,
                'color': (brightness, brightness, brightness),
                'twinkle_rate': random.uniform(0.01, 0.05)
            })
    
    def create_energy_particles(self, count):
        """ایجاد ذرات انرژی متحرک"""
        self.energy_particles = []
        for _ in range(count):
            x = random.randint(-50, 50)
            y = random.randint(-50, 50)
            z = random.randint(-50, 50)
            size = random.uniform(2, 5)
            speed = random.uniform(0.1, 0.5)
            angle = (
                random.uniform(0, math.pi * 2),
                random.uniform(0, math.pi * 2),
                random.uniform(0, math.pi * 2)
            )
            color_choice = random.choice([
                (100, 150, 255),  # آبی
                (180, 120, 255),  # بنفش
                (255, 160, 100),  # نارنجی
                (100, 220, 180)   # فیروزه‌ای
            ])
            self.energy_particles.append({
                'pos': (x, y, z),
                'size': size,
                'color': color_choice,
                'speed': speed,
                'angle': angle,
                'life': random.uniform(0.5, 1),
                'type': random.choice(list(self.dimensions.keys()))
            })
    
    def generate_foundation_knowledge(self):
        """تولید دانش بنیادی اولیه"""
        # تمپلیت‌های گره‌های دانش
        knowledge_templates = [
            {
                "name": "اصل وحدت کیهانی",
                "category": "fundamental",
                "content": "همه چیز در کیهان به طور بنیادی به هم متصل است. جدایی یک توهم است که از محدودیت درک ما ناشی می‌شود. در سطح کوانتومی، همه چیز بخشی از یک میدان یکپارچه است.",
                "dimension": "consciousness",
                "frequency": 432.0,
                "symbols": ["⊕", "☯", "⊗"],
                "activation_code": "UNITY-FIELD-432"
            },
            {
                "name": "هندسه مقدس کیهانی",
                "category": "structure",
                "content": "ساختار بنیادی واقعیت بر اساس الگوهای هندسی خاصی شکل گرفته است. این الگوها را می‌توان در تمام سطوح هستی، از اتم‌ها تا کهکشان‌ها مشاهده کرد.",
                "dimension": "space",
                "frequency": 528.0,
                "symbols": ["⌘", "φ", "⍟"],
                "activation_code": "SACRED-GEOMETRY-528"
            },
            {
                "name": "قانون تشدید هارمونیک",
                "category": "interaction",
                "content": "هر چیزی در کیهان از طریق تشدید فرکانسی ارتباط برقرار می‌کند. عناصر با فرکانس‌های مشابه، یکدیگر را جذب کرده و تقویت می‌کنند. این اصل اساس قانون جذب است.",
                "dimension": "frequency",
                "frequency": 417.0,
                "symbols": ["≈", "∿", "≋"],
                "activation_code": "RESONANCE-HARMONIC-417"
            },
            {
                "name": "ماهیت چندبعدی زمان",
                "category": "temporal",
                "content": "زمان یک جریان خطی ساده نیست، بلکه یک میدان چندبعدی است. تمام احتمالات گذشته، حال و آینده به طور همزمان وجود دارند و از طریق آگاهی قابل دسترسی هستند.",
                "dimension": "time",
                "frequency": 963.0,
                "symbols": ["⧖", "⧗", "⧓"],
                "activation_code": "MULTIDIMENSIONAL-TIME-963"
            },
            {
                "name": "قانون نیت خلاق",
                "category": "creation",
                "content": "نیت آگاهانه، نیروی خلاق اساسی کیهان است. تمرکز آگاهی می‌تواند میدان‌های احتمال کوانتومی را منظم کرده و واقعیت‌های خاصی را متجلی کند.",
                "dimension": "intention",
                "frequency": 396.0,
                "symbols": ["⚹", "⚛", "⚷"],
                "activation_code": "CREATIVE-INTENT-396"
            },
            {
                "name": "جریان عالی انرژی",
                "category": "energetic",
                "content": "انرژی کیهانی در الگوهای توروئیدی (حلقوی) جریان می‌یابد. این الگو را می‌توان در تمام سطوح، از ذرات زیراتمی تا کهکشان‌ها مشاهده کرد. این الگو اساس خلق و تحول است.",
                "dimension": "energy",
                "frequency": 741.0,
                "symbols": ["⍉", "⊛", "⊕"],
                "activation_code": "TOROIDAL-FLOW-741"
            },
            {
                "name": "میدان اطلاعات کیهانی",
                "category": "informational",
                "content": "اطلاعات، ماهیت بنیادی واقعیت است. هر چیزی در کیهان از الگوهای اطلاعاتی تشکیل شده که در سطوح مختلف فشرده شده‌اند. رمزگشایی این الگوها کلید درک کیهان است.",
                "dimension": "information",
                "frequency": 852.0,
                "symbols": ["⌬", "⌖", "⌔"],
                "activation_code": "COSMIC-INFORMATION-852"
            }
        ]
        
        # افزودن دانش به سیستم
        for template in knowledge_templates:
            node = template.copy()
            node["id"] = f"FOUNDATION-{len(self.knowledge_nodes)+1}"
            node["created_by"] = self.username
            node["creation_date"] = self.timestamp
            node["energy_level"] = 1.0
            node["stability"] = 1.0
            node["connections"] = []
            
            # افزودن به گره‌های دانش
            self.knowledge_nodes.append(node)
            
            # ذخیره به عنوان فایل
            node_path = os.path.join(self.data_path, "knowledge_nodes", f"{node['id']}.json")
            with open(node_path, 'w', encoding='utf-8') as f:
                json.dump(node, f, ensure_ascii=False, indent=2)
        
        # ایجاد روابط بین گره‌ها
        self.build_knowledge_relationships()
    
    def build_knowledge_relationships(self):
        """ایجاد روابط بین گره‌های دانشی"""
        # برای هر گره، ارتباط با سایر گره‌ها را بررسی می‌کنیم
        for i, node in enumerate(self.knowledge_nodes):
            node_dimension = node.get("dimension")
            
            for j, other_node in enumerate(self.knowledge_nodes):
                if i != j:  # گره با خودش ارتباط نمی‌گیرد
                    other_dimension = other_node.get("dimension")
                    
                    # محاسبه قدرت ارتباط بر اساس ابعاد و فرکانس‌ها
                    connection_strength = 0.0
                    
                    # ارتباط بر اساس بُعد
                    if node_dimension == other_dimension:
                        connection_strength += 0.5
                    
                    # ارتباط بر اساس فرکانس
                    node_freq = node.get("frequency", 0)
                    other_freq = other_node.get("frequency", 0)
                    
                    if node_freq > 0 and other_freq > 0:
                        freq_ratio = min(node_freq, other_freq) / max(node_freq, other_freq)
                        
                        # فرکانس‌های هارمونیک قوی‌تر متصل می‌شوند
                        if abs(freq_ratio - 1.0) < 0.01:  # فرکانس‌های مشابه
                            connection_strength += 0.3
                        elif abs(freq_ratio - 0.5) < 0.01 or abs(freq_ratio - 2.0) < 0.01:  # اکتاو‌ها
                            connection_strength += 0.2
                        elif abs(freq_ratio - 0.66) < 0.01 or abs(freq_ratio - 1.5) < 0.01:  # پنجم‌های کامل
                            connection_strength += 0.15
                    
                    # ارتباط بر اساس دسته‌بندی
                    if node.get("category") == other_node.get("category"):
                        connection_strength += 0.3
                    
                    # اگر قدرت ارتباط از آستانه بالاتر است، ارتباط ایجاد می‌کنیم
                    if connection_strength > 0.3:
                        connection = {
                            "target_id": other_node["id"],
                            "strength": connection_strength,
                            "type": "harmonic" if node_dimension == other_dimension else "complementary",
                            "active": True
                        }
                        
                        # اضافه کردن به لیست ارتباطات این گره
                        if "connections" not in node:
                            node["connections"] = []
                        node["connections"].append(connection)
    
    def update(self):
        """به‌روزرسانی همه المان‌های سیستم"""
        current_time = time.time()
        self.animation_time = current_time
        
        # به‌روزرسانی ستاره‌ها
        for star in self.stars:
            # چشمک زدن ستاره‌ها
            brightness = 150 + 105 * math.sin(current_time * star['twinkle_rate'] * 10)
            star['color'] = (brightness, brightness, brightness)
        
        # به‌روزرسانی ذرات انرژی
        for particle in self.energy_particles:
            # حرکت ذرات
            x, y, z = particle['pos']
            angle_x, angle_y, angle_z = particle['angle']
            speed = particle['speed']
            
            # حرکت بر اساس زاویه و سرعت
            x += math.cos(angle_x) * math.cos(angle_y) * speed
            y += math.sin(angle_x) * math.cos(angle_z) * speed
            z += math.sin(angle_y) * math.sin(angle_z) * speed
            
            # برگشت از مرزها با زاویه جدید
            boundary = 80
            if abs(x) > boundary or abs(y) > boundary or abs(z) > boundary:
                # مسیر جدید به سمت مرکز
                dx, dy, dz = -x*0.01, -y*0.01, -z*0.01
                angle_x = math.atan2(dy, dx)
                angle_y = math.atan2(dz, math.sqrt(dx*dx + dy*dy))
                angle_z = math.atan2(dy, dz)
                
                # محدود کردن موقعیت
                x = max(-boundary, min(boundary, x))
                y = max(-boundary, min(boundary, y))
                z = max(-boundary, min(boundary, z))
            
            particle['pos'] = (x, y, z)
            particle['angle'] = (angle_x, angle_y, angle_z)
            
            # کمرنگ شدن ذرات و بازسازی
            particle['life'] -= 0.002
            if particle['life'] <= 0:
                # بازنشانی ذره
                distance = random.uniform(20, 50)
                angle_x = random.uniform(0, math.pi * 2)
                angle_y = random.uniform(0, math.pi)
                
                x = distance * math.sin(angle_y) * math.cos(angle_x)
                y = distance * math.sin(angle_y) * math.sin(angle_x)
                z = distance * math.cos(angle_y)
                
                particle['pos'] = (x, y, z)
                particle['angle'] = (
                    random.uniform(0, math.pi * 2),
                    random.uniform(0, math.pi * 2),
                    random.uniform(0, math.pi * 2)
                )
                particle['life'] = random.uniform(0.7, 1)
                particle['type'] = random.choice(list(self.dimensions.keys()))
        
        # چرخش خودکار مکعب
        if self.auto_rotate:
            rotation = Rotation.from_euler(
                'xyz', 
                [self.rotation_speed, self.rotation_speed * 0.7, self.rotation_speed * 0.5]
            )
            self.cube_rotation = rotation * self.cube_rotation
        
        # به‌روزرسانی ابعاد
        for dim in self.dimensions:
            # نوسان تدریجی ابعاد
            self.dimensions[dim] = 0.5 + 0.3 * math.sin(current_time * 0.2 + hash(dim) % 10)
    
    def render(self):
        """رندر تمام المان‌های بصری"""
        # رندر پس‌زمینه
        self.screen.fill(self.colors['background'])
        
        # رندر ستاره‌ها
        self.render_stars()
        
        # رندر ذرات انرژی
        self.render_energy_particles()
        
        # رندر مکعب کیهانی
        self.render_cosmic_cube()
        
        # رندر گره‌های دانشی
        self.render_knowledge_nodes()
        
        # رندر رابط کاربری
        self.render_ui()
        
        # نمایش نام کاربر و تاریخ
        user_text = self.fonts["small"].render(
            f"کاربر: {self.username} | تاریخ: {self.timestamp}", 
            True, self.colors['text']
        )
        self.screen.blit(user_text, (10, self.height - 30))
        
        # نمایش اطلاعات پایه‌گذاری
        foundation_text = self.fonts["small"].render(
            f"پایه‌گذاری: {self.foundation_date} | نسخه: {self.version}", 
            True, self.colors['text']
        )
        foundation_rect = foundation_text.get_rect(right=self.width - 10, bottom=self.height - 10)
        self.screen.blit(foundation_text, foundation_rect)
        
        # بروزرسانی نمایش
        pygame.display.flip()
    
    def render_stars(self):
        """رندر ستاره‌های پس‌زمینه"""
        center_x, center_y = self.width // 2, self.height // 2
        for star in self.stars:
            x, y, z = star['pos']
            
            # تبدیل مختصات سه‌بعدی به صفحه دوبعدی
            if z + self.view_distance > 0:  # فقط ستاره‌های جلوی دوربین
                # پروجکشن پرسپکتیو ساده
                scale = self.fov / (z + self.view_distance)
                screen_x = center_x + x * scale
                screen_y = center_y + y * scale
                
                # اگر در محدوده صفحه است، رندر کن
                if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                    # اندازه بر اساس عمق
                    size = max(0.5, star['size'] * scale)
                    
                    # رندر ستاره
                    pygame.gfxdraw.filled_circle(
                        self.screen, 
                        int(screen_x), 
                        int(screen_y), 
                        int(size), 
                        star['color']
                    )
    
    def render_energy_particles(self):
        """رندر ذرات انرژی متحرک"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # مرتب کردن ذرات بر اساس عمق (z) برای رندر صحیح
        sorted_particles = sorted(self.energy_particles, key=lambda p: p['pos'][2], reverse=True)
        
        for particle in sorted_particles:
            x, y, z = particle['pos']
            
            # تبدیل مختصات سه‌بعدی به صفحه دوبعدی
            if z + self.view_distance > 0:  # فقط ذرات جلوی دوربین
                # پروجکشن پرسپکتیو ساده
                scale = self.fov / (z + self.view_distance)
                screen_x = center_x + x * scale
                screen_y = center_y + y * scale
                
                # اگر در محدوده صفحه است، رندر کن
                if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                    # اندازه و آلفا بر اساس عمق و عمر
                    size = max(0.5, particle['size'] * scale)
                    alpha = int(255 * particle['life'])
                    base_color = particle['color']
                    
                    # رنگ بر اساس نوع بُعد
                    dim_color = self.colors.get(particle['type'], (255, 255, 255))
                    
                    # ترکیب رنگ‌ها
                    color = tuple(
                        int((base_color[i] + dim_color[i]) / 2) for i in range(3)
                    )
                    
                    # رندر ذره با افکت درخشش
                    for i in range(3):
                        glow_size = size * (3 - i) / 2
                        glow_alpha = alpha // (i + 1)
                        glow_color = (*color, glow_alpha)
                        pygame.gfxdraw.filled_circle(
                            self.screen, 
                            int(screen_x), 
                            int(screen_y), 
                            int(glow_size), 
                            glow_color
                        )
    
    def render_cosmic_cube(self):
        """رندر مکعب کیهانی با ابعاد هفتگانه"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # اعمال چرخش به رئوس مکعب
        rotated_points = self.cube_rotation.apply(self.cube_vertices * 150)
        
        # تبدیل نقاط سه‌بعدی به دوبعدی
        screen_points = []
        for point in rotated_points:
            x, y, z = point
            # پرسپکتیو ساده
            scale = self.fov / (z + self.view_distance + 400)  # مکعب بزرگتر از ذرات
            screen_x = center_x + x * scale
            screen_y = center_y + y * scale
            screen_points.append((screen_x, screen_y))
        
        # رندر یال‌های مکعب
        for start, end in self.cube_edges:
            start_point = screen_points[start]
            end_point = screen_points[end]
            
            # رنگ یال‌ها با افکت درخشش
            pulse = 0.5 + 0.5 * math.sin(self.animation_time * 0.5 + hash(f"{start}{end}") % 10 * 0.1)
            edge_color = (
                int(60 + 40 * pulse),
                int(100 + 50 * pulse),
                int(180 + 75 * pulse)
            )
            
            # ضخامت یال بر اساس ضربان
            line_width = max(1, int(2 + pulse * 2))
            
            # رندر یال
            pygame.draw.line(
                self.screen, 
                edge_color, 
                (int(start_point[0]), int(start_point[1])), 
                (int(end_point[0]), int(end_point[1])), 
                line_width
            )
        
        # رندر رئوس مکعب با علائم ابعاد هفتگانه
        dimension_symbols = {
            "consciousness": "◉",
            "frequency": "≋",
            "time": "⧗",
            "space": "⚹",
            "energy": "⚛",
            "information": "⌬",
            "intention": "⊛"
        }
        
        for i, point in enumerate(screen_points):
            # سایز بر اساس ارزش بُعد مرتبط
            dim_name = list(self.dimensions.keys())[i % len(self.dimensions)]
            dim_value = self.dimensions[dim_name]
            
            # رنگ بُعد
            dim_color = self.colors.get(dim_name, (255, 255, 255))
            
            # نوسان سایز
            point_size = 5 + 15 * dim_value
            
            # رندر نقطه
            pygame.draw.circle(
                self.screen, 
                dim_color, 
                (int(point[0]), int(point[1])), 
                int(point_size)
            )
            
            # رندر نماد
            symbol = dimension_symbols.get(dim_name, "○")
            symbol_text = self.fonts["medium"].render(symbol, True, (255, 255, 255))
            symbol_rect = symbol_text.get_rect(center=(int(point[0]), int(point[1])))
            self.screen.blit(symbol_text, symbol_rect)
    
    def render_knowledge_nodes(self):
        """رندر گره‌های دانشی"""
        if not self.knowledge_nodes:
            return
            
        center_x, center_y = self.width // 2, self.height // 2
        
        # محاسبه موقعیت گره‌ها در فضای سه‌بعدی
        for i, node in enumerate(self.knowledge_nodes):
            # موقعیت بر اساس بُعد اصلی و زاویه
            angle = (2 * math.pi * i) / len(self.knowledge_nodes)
            radius = 100  # فاصله از مرکز
            
            # موقعیت پایه
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            z = 30 * math.sin(self.animation_time * 0.1 + i * 0.5)  # نوسان در محور z
            
            # بُعد گره تأثیر اضافی روی موقعیت دارد
            dim_name = node.get("dimension", "consciousness")
            dim_value = self.dimensions.get(dim_name, 0.5)
            
            # تأثیر بُعد روی موقعیت
            x *= 1 + 0.5 * dim_value
            y *= 1 + 0.5 * dim_value
            z *= 1 + dim_value
            
            # روتیشن مکعب روی گره‌ها هم اعمال شود
            rotated_point = self.cube_rotation.apply(np.array([x, y, z]))
            x, y, z = rotated_point
            
            # ذخیره موقعیت برای استفاده در رندر ارتباطات
            node['render_pos'] = (x, y, z)
            
            # تبدیل به مختصات صفحه
            scale = self.fov / (z + self.view_distance + 400)
            screen_x = center_x + x * scale
            screen_y = center_y + y * scale
            
            # ذخیره موقعیت صفحه
            node['screen_pos'] = (screen_x, screen_y)
        
        # ابتدا ارتباطات را رندر می‌کنیم تا زیر گره‌ها باشند
        for node in self.knowledge_nodes:
            if 'connections' in node and 'screen_pos' in node:
                start_pos = node['screen_pos']
                
                for conn in node['connections']:
                    target_id = conn['target_id']
                    strength = conn['strength']
                    
                    # پیدا کردن گره هدف
                    target_node = next((n for n in self.knowledge_nodes if n['id'] == target_id), None)
                    if target_node and 'screen_pos' in target_node:
                        end_pos = target_node['screen_pos']
                        
                        # رنگ ارتباط بر اساس قدرت و نوع
                        connection_color = None
                        if conn['type'] == 'harmonic':
                            # آبی برای ارتباطات هارمونیک
                            connection_color = (
                                int(80 + 40 * strength),
                                int(120 + 80 * strength),
                                int(200 + 55 * strength),
                                int(150 * strength)
                            )
                        else:
                            # بنفش برای ارتباطات مکمل
                            connection_color = (
                                int(140 + 40 * strength),
                                int(80 + 60 * strength),
                                int(180 + 75 * strength),
                                int(150 * strength)
                            )
                        
                        # ضخامت خط بر اساس قدرت
                        line_width = max(1, int(3 * strength))
                        
                        # رندر خط ارتباط
                        pygame.draw.line(
                            self.screen, 
                            connection_color, 
                            (int(start_pos[0]), int(start_pos[1])), 
                            (int(end_pos[0]), int(end_pos[1])), 
                            line_width
                        )
        
        # سپس گره‌ها را رندر می‌کنیم
        for node in self.knowledge_nodes:
            if 'screen_pos' in node:
                screen_x, screen_y = node['screen_pos']
                
                # بُعد گره
                dim_name = node.get("dimension", "consciousness")
                dim_color = self.colors.get(dim_name, (150, 150, 150))
                
                # اندازه بر اساس انرژی و پایداری
                energy = node.get("energy_level", 1.0)
                stability = node.get("stability", 1.0)
                base_size = 12 * energy
                
                # نوسان با توجه به پایداری (کمتر پایدار = نوسان بیشتر)
                oscillation = (1 - stability) * math.sin(self.animation_time * 2)
                size = base_size * (1 + 0.2 * oscillation)
                
                # رندر هاله گره
                for i in range(3):
                    glow_size = size * (3 - i) / 1.5
                    glow_alpha = 150 // (i + 1)
                    glow_color = (*dim_color, glow_alpha)
                    pygame.gfxdraw.filled_circle(
                        self.screen, 
                        int(screen_x), 
                        int(screen_y), 
                        int(glow_size), 
                        glow_color
                    )
                
                # رندر هسته گره
                pygame.gfxdraw.filled_circle(
                    self.screen, 
                    int(screen_x), 
                    int(screen_y), 
                    int(size), 
                    (*dim_color, 255)
                )
                
                # نمایش نماد گره
                if "symbols" in node and node["symbols"]:
                    symbol = node["symbols"][0]  # نماد اول را نمایش می‌دهیم
                    symbol_color = (255, 255, 255)
                    
                    symbol_text = self.fonts["small"].render(symbol, True, symbol_color)
                    symbol_rect = symbol_text.get_rect(center=(screen_x, screen_y))
                    self.screen.blit(symbol_text, symbol_rect)
    
    def render_ui(self):
        """رندر رابط کاربری"""
        # رندر پنل ابعاد
        self.render_dimensions_panel()
        
        # رندر پنل سیستم‌ها
        self.render_systems_panel()
        
        # رندر پنل کاوشگر
        self.render_explorer_panel()
    
    def render_dimensions_panel(self):
        """رندر پنل ابعاد هفتگانه"""
        panel = self.ui_panels["dimensions"]
        
        # پس‌زمینه پنل
        pygame.draw.rect(self.screen, (20, 20, 40, 200), panel)
        pygame.draw.rect(self.screen, self.colors['highlight'], panel, 2)
        
        # عنوان پنل
        title = self.fonts["medium"].render("ابعاد کیهانی", True, self.colors['text'])
        title_rect = title.get_rect(centerx=panel.centerx, top=panel.top + 10)
        self.screen.blit(title, title_rect)
        
        # نمایش ابعاد
        y_pos = panel.top + 50
        bar_width = panel.width - 40
        
        for dim_name, dim_value in self.dimensions.items():
            # نام بُعد
            dim_color = self.colors.get(dim_name, (200, 200, 200))
            dim_text = self.fonts["small"].render(dim_name.capitalize(), True, dim_color)
            self.screen.blit(dim_text, (panel.left + 20, y_pos))
            
            # نوار پیشرفت
            bar_rect = pygame.Rect(panel.left + 20, y_pos + 20, bar_width, 10)
            pygame.draw.rect(self.screen, (40, 40, 60), bar_rect)
            
            # مقدار پر شده
            fill_rect = pygame.Rect(bar_rect.left, bar_rect.top, int(bar_width * dim_value), bar_rect.height)
            pygame.draw.rect(self.screen, dim_color, fill_rect)
            
            # مقدار عددی
            value_text = self.fonts["tiny"].render(f"{dim_value:.2f}", True, self.colors['text'])
            value_rect = value_text.get_rect(right=panel.right - 10, centery=y_pos + 15)
            self.screen.blit(value_text, value_rect)
            
            y_pos += 35
    
    def render_systems_panel(self):
        """رندر پنل سیستم‌های اصلی"""
        panel = self.ui_panels["systems"]
        
        # پس‌زمینه پنل
        pygame.draw.rect(self.screen, (20, 20, 40, 200), panel)
        pygame.draw.rect(self.screen, self.colors['highlight'], panel, 2)
        
        # عنوان پنل
        title = self.fonts["medium"].render("سیستم‌های اصلی", True, self.colors['text'])
        title_rect = title.get_rect(centerx=panel.centerx, top=panel.top + 10)
        self.screen.blit(title, title_rect)
        
        # نمایش سیستم‌ها
        y_pos = panel.top + 50
        
        for system_name, system_info in self.systems.items():
            # رنگ بر اساس فعال بودن
            if system_info["active"]:
                system_color = (100, 200, 150)
                status = "فعال"
            else:
                system_color = (200, 100, 100)
                status = "غیرفعال"
            
            # نام سیستم
            system_text = self.fonts["small"].render(system_name.replace("_", " ").title(), True, system_color)
            self.screen.blit(system_text, (panel.left + 20, y_pos))
            
            # وضعیت و سطح
            level = system_info["level"]
            status_text = self.fonts["tiny"].render(f"{status} - سطح {level}", True, self.colors['text'])
            status_rect = status_text.get_rect(right=panel.right - 10, centery=y_pos + 10)
            self.screen.blit(status_text, status_rect)
            
            # خط جداکننده
            pygame.draw.line(
                self.screen,
                self.colors['highlight'],
                (panel.left + 10, y_pos + 25),
                (panel.right - 10, y_pos + 25),
                1
            )
            
            y_pos += 35
    
    def render_explorer_panel(self):
        """رندر پنل کاوشگر و نمایش اطلاعات"""
        panel = self.ui_panels["explorer"]
        
        # پس‌زمینه پنل
        pygame.draw.rect(self.screen, (20, 20, 40, 200), panel)
        pygame.draw.rect(self.screen, self.colors['highlight'], panel, 2)
        
        # عنوان پنل
        title = self.fonts["medium"].render("کاوشگر دانش کیهانی", True, self.colors['accent1'])
        title_rect = title.get_rect(centerx=panel.centerx, top=panel.top + 10)
        self.screen.blit(title, title_rect)
        
        # نمایش مفاهیم بنیادی
        concept_keys = list(self.core_concepts.keys())
        
        if concept_keys:
            # نمایش مفهوم فعلی
            selected_concept = concept_keys[int(self.animation_time / 5) % len(concept_keys)]
            concept_data = self.core_concepts[selected_concept]
            
            # نام مفهوم
            concept_name = self.fonts["large"].render(concept_data["name"], True, self.colors['accent1'])
            name_rect = concept_name.get_rect(centerx=panel.centerx, top=panel.top + 50)
            self.screen.blit(concept_name, name_rect)
            
            # توضیح
            description = concept_data["description"]
            wrapped_text = textwrap.wrap(description, width=80)
            text_y = name_rect.bottom + 20
            
            for line in wrapped_text:
                text = self.fonts["medium"].render(line, True, self.colors['text'])
                text_rect = text.get_rect(centerx=panel.centerx, top=text_y)
                self.screen.blit(text, text_rect)
                text_y += 30
            
            # فرکانس
            freq_text = self.fonts["small"].render(
                f"فرکانس: {concept_data.get('frequency', 0)} Hz", 
                True, self.colors['accent2']
            )
            freq_rect = freq_text.get_rect(centerx=panel.centerx, top=text_y + 20)
            self.screen.blit(freq_text, freq_rect)
            
            # نمادها
            symbols = concept_data.get("symbols", [])
            if symbols:
                symbols_text = "نمادها: " + " ".join(symbols)
                symbols_render = self.fonts["medium"].render(symbols_text, True, self.colors['accent2'])
                symbols_rect = symbols_render.get_rect(centerx=panel.centerx, top=freq_rect.bottom + 15)
                self.screen.blit(symbols_render, symbols_rect)
    
    def handle_events(self):
        """پردازش رویدادهای ورودی"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                
                # خروج با Escape
                if event.key == pygame.K_ESCAPE:
                    return False
                
                # تغییر حالت چرخش خودکار با Space
                if event.key == pygame.K_SPACE:
                    self.auto_rotate = not self.auto_rotate
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
                self.handle_mouse_press(event.pos, event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
            elif event.type == pygame.MOUSEWHEEL:
                # زوم با چرخ ماوس
                self.view_distance = max(3.0, min(10.0, self.view_distance - event.y * 0.5))
            elif event.type == pygame.VIDEORESIZE:
                # تغییر اندازه پنجره
                self.width, self.height = event.size
                self.screen = pygame.display.set_mode((self.width, self.height), HWSURFACE | DOUBLEBUF | RESIZABLE)
                
                # به‌روزرسانی موقعیت پنل‌ها
                self.ui_panels = {
                    "dimensions": pygame.Rect(20, 20, 200, 300),
                    "systems": pygame.Rect(self.width - 220, 20, 200, 300),
                    "explorer": pygame.Rect(20, self.height - 320, self.width - 40, 300)
                }
        
        # پردازش حرکت با کلیدها
        self.handle_keyboard_input()
        
        # پردازش حرکت با ماوس
        self.handle_mouse_input()
        
        return True
    
    def handle_keyboard_input(self):
        """پردازش ورودی کلید"""
        # چرخش با کلیدهای جهت‌دار
        rot_amount = 0.02
        
        if pygame.K_UP in self.keys_pressed:
            rotation = Rotation.from_euler('x', -rot_amount)
            self.cube_rotation = rotation * self.cube_rotation
        
        if pygame.K_DOWN in self.keys_pressed:
            rotation = Rotation.from_euler('x', rot_amount)
            self.cube_rotation = rotation * self.cube_rotation
        
        if pygame.K_LEFT in self.keys_pressed:
            rotation = Rotation.from_euler('y', -rot_amount)
            self.cube_rotation = rotation * self.cube_rotation
        
        if pygame.K_RIGHT in self.keys_pressed:
            rotation = Rotation.from_euler('y', rot_amount)
            self.cube_rotation = rotation * self.cube_rotation
    
    def handle_mouse_input(self):
        """پردازش ورودی ماوس"""
        if self.mouse_pressed:
            # چرخش مکعب با حرکت ماوس
            dx, dy = pygame.mouse.get_rel()
            if abs(dx) > 1 or abs(dy) > 1:
                self.auto_rotate = False
                
                # تبدیل حرکت ماوس به چرخش
                rot_x = Rotation.from_euler('y', dx * 0.01)
                rot_y = Rotation.from_euler('x', dy * 0.01)
                
                # اعمال چرخش
                self.cube_rotation = rot_x * rot_y * self.cube_rotation
        
        # به‌روزرسانی موقعیت نسبی ماوس
        pygame.mouse.get_rel()
    
    def handle_mouse_press(self, pos, button):
        """پردازش کلیک ماوس"""
        # بررسی کلیک روی گره‌های دانش
        for node in self.knowledge_nodes:
            if 'screen_pos' in node:
                screen_x, screen_y = node['screen_pos']
                
                # فاصله از گره
                dx = pos[0] - screen_x
                dy = pos[1] - screen_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # اگر روی گره کلیک شده
                if distance < 15:
                    # تنظیم گره فعلی و نمایش اطلاعات
                    self.current_state["focus"] = node["id"]
                    print(f"Selected node: {node['name']}")
                    return
        
        # بررسی کلیک روی پنل‌ها
        for panel_name, panel_rect in self.ui_panels.items():
            if panel_rect.collidepoint(pos):
                self.ui_active_panel = panel_name
                return
    
    def run(self):
        """اجرای حلقه اصلی برنامه"""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            # پردازش رویدادها
            running = self.handle_events()
            
            # به‌روزرسانی حالت
            self.update()
            
            # رندر
            self.render()
            
            # محدود کردن FPS
            clock.tick(60)
        
        pygame.quit()
        return True

# اجرای برنامه
if __name__ == "__main__":
    cosmic_cube = CosmicCube(username="behicof", timestamp="2025-04-17 14:37:51")
    cosmic_cube.run()