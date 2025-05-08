import pygame
import random
import math
import json
import os
import time
from datetime import datetime
from dataclasses import dataclass, asdict

# Reality Editor Core
@dataclass
class RealityRule:
    value: str
    time: str
    risk: str
    dimension: str = "3D"
    causality: str = "forward"
    probability: str = "quantum"
    observer: str = "conscious"

class RealityForge:
    def __init__(self, username="behicof", timestamp=None):
        self.username = username
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.saved_realities = []
        self.reality_history = []
        
        # Default reality configuration
        self.current_rules = RealityRule(
            value="dynamic",
            time="linear",
            risk="real",
            dimension="3D",
            causality="forward",
            probability="quantum",
            observer="conscious"
        )
        
        # Load saved realities
        self.load_saved_realities()
        
        # Record starting reality
        self.reality_history.append({
            "rules": asdict(self.current_rules),
            "timestamp": self.timestamp,
            "username": self.username
        })
    
    def rewrite_rules(self, new_rules):
        """Alter fundamental reality parameters"""
        changed = False
        for field, value in new_rules.items():
            if hasattr(self.current_rules, field):
                old_value = getattr(self.current_rules, field)
                setattr(self.current_rules, field, value)
                changed = changed or (old_value != value)
        
        if changed:
            # Record the change in history
            self.reality_history.append({
                "rules": asdict(self.current_rules),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": self.username
            })
            
        return {
            "status": "reality_updated" if changed else "no_change",
            "current_rules": asdict(self.current_rules)
        }
    
    def save_reality(self, name, description):
        """Save current reality configuration"""
        reality_data = {
            "name": name,
            "description": description,
            "rules": asdict(self.current_rules),
            "created_by": self.username,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "id": str(int(time.time()))
        }
        
        # Save to file
        filepath = os.path.join("cosmic_data", "Reality_Configurations", f"{reality_data['id']}.json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(reality_data, f, indent=2, ensure_ascii=False)
        
        self.saved_realities.append(reality_data)
        return reality_data
    
    def load_saved_realities(self):
        """Load all saved reality configurations"""
        self.saved_realities = []
        directory = os.path.join("cosmic_data", "Reality_Configurations")
        
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            return
        
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.saved_realities.append(data)
                except Exception as e:
                    print(f"Error loading reality configuration: {e}")
        
        # Sort by timestamp (newest first)
        self.saved_realities.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    def apply_saved_reality(self, reality_id):
        """Apply a saved reality configuration"""
        for reality in self.saved_realities:
            if reality.get("id") == reality_id:
                rules = reality.get("rules", {})
                return self.rewrite_rules(rules)
        
        return {"status": "error", "message": "Reality configuration not found"}
    
    def export_reality_history(self, filepath=None):
        """Export the reality modification history to a file"""
        if filepath is None:
            filepath = f"reality_history_{int(time.time())}.json"
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.reality_history, f, indent=2, ensure_ascii=False)
        
        return {"status": "exported", "filepath": filepath}

# Reality Visualization System
class CosmicRealityVisualizer:
    def __init__(self, forge=None):
        pygame.init()
        self.width, self.height = 1280, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cosmic Reality Forge")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Reality Forge
        self.forge = forge or RealityForge()
        
        # Fonts
        self.font_tiny = pygame.font.SysFont('Arial', 12)
        self.font_small = pygame.font.SysFont('Arial', 16)
        self.font = pygame.font.SysFont('Arial', 24)
        self.font_medium = pygame.font.SysFont('Arial', 28)
        self.font_large = pygame.font.SysFont('Arial', 36)
        
        # Colors
        self.colors = {
            'background': (5, 10, 30),
            'text': (220, 220, 255),
            'highlight': (100, 100, 200),
            'accent1': (180, 120, 255),
            'accent2': (100, 200, 220),
            'button': (40, 40, 80),
            'button_highlight': (60, 60, 120),
            'panel': (20, 20, 40, 220),
            'success': (100, 200, 100),
            'warning': (200, 150, 50),
            'tag': (60, 80, 120),
            'value': (100, 200, 255),
            'time': (200, 150, 255),
            'risk': (255, 150, 100),
            'dimension': (150, 255, 150),
            'causality': (255, 200, 100),
            'probability': (150, 200, 255),
            'observer': (255, 150, 200)
        }
        
        # Visual elements
        self.stars = []
        self.energy_particles = []
        self.create_stars(300)
        self.create_energy_particles(80)
        
        # UI state
        self.active_view = "main"  # "main", "edit", "saved", "detail"
        self.editing_field = None
        self.editing_text = ""
        self.selected_reality = None
        self.save_mode = False
        self.save_name = ""
        self.save_description = ""
        self.save_field = "name"
        
        # Notification system
        self.notification = None
        self.notification_timer = 0
        
        # Animation elements
        self.animation_time = 0
        self.particles = []
        
        # Reality field options
        self.field_options = {
            "value": ["dynamic", "static", "cyclical", "quantum", "relative"],
            "time": ["linear", "cyclical", "branching", "quantum", "reversed"],
            "risk": ["real", "perceived", "eliminated", "probability-based", "reverse-correlated"],
            "dimension": ["3D", "4D", "2D", "5D", "multidimensional"],
            "causality": ["forward", "backward", "bidirectional", "non-linear", "quantum"],
            "probability": ["quantum", "deterministic", "wave-based", "observer-dependent", "multiversal"],
            "observer": ["conscious", "unconscious", "collective", "quantum", "universal"]
        }
    
    def create_stars(self, count):
        self.stars = []
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.uniform(0.5, 2.5)
            brightness = random.uniform(100, 255)
            self.stars.append({
                'pos': (x, y),
                'size': size,
                'color': (brightness, brightness, brightness),
                'twinkle_rate': random.uniform(0.01, 0.05)
            })
    
    def create_energy_particles(self, count):
        self.energy_particles = []
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.uniform(2, 4)
            speed = random.uniform(0.5, 2)
            angle = random.uniform(0, math.pi * 2)
            color_choice = random.choice([
                (100, 150, 255),  # Blue
                (180, 120, 255),  # Purple
                (255, 160, 100),  # Orange
                (100, 220, 180)   # Teal
            ])
            self.energy_particles.append({
                'pos': (x, y),
                'size': size,
                'color': color_choice,
                'speed': speed,
                'angle': angle,
                'life': random.uniform(0.5, 1)
            })
    
    def update_stars(self):
        for star in self.stars:
            # Make stars twinkle
            brightness = 150 + 105 * math.sin(time.time() * star['twinkle_rate'] * 10)
            star['color'] = (brightness, brightness, brightness)
    
    def update_energy_particles(self):
        for particle in self.energy_particles:
            # Move particles
            x, y = particle['pos']
            angle = particle['angle']
            speed = particle['speed']
            
            # Update position based on angle and speed
            x += math.cos(angle) * speed
            y += math.sin(angle) * speed
            
            # Bounce off edges with new angle
            if x < 0 or x > self.width:
                angle = math.pi - angle
                x = max(0, min(x, self.width))
            if y < 0 or y > self.height:
                angle = -angle
                y = max(0, min(y, self.height))
                
            particle['pos'] = (x, y)
            particle['angle'] = angle
            
            # Fade particles over time and regenerate
            particle['life'] -= 0.005
            if particle['life'] <= 0:
                # Reset particle
                particle['pos'] = (random.randint(0, self.width), random.randint(0, self.height))
                particle['angle'] = random.uniform(0, math.pi * 2)
                particle['life'] = random.uniform(0.5, 1)
    
    def create_reality_change_particles(self, num_particles=100):
        """Create particles for reality change animation"""
        self.particles = []
        center_x, center_y = self.width // 2, self.height // 2
        
        for _ in range(num_particles):
            angle = random.uniform(0, math.pi * 2)
            distance = random.uniform(50, 400)
            speed = random.uniform(2, 6)
            size = random.uniform(2, 5)
            
            particle_type = random.choice(list(self.field_options.keys()))
            color = self.colors.get(particle_type, (255, 255, 255))
            
            self.particles.append({
                'pos': (center_x, center_y),
                'angle': angle,
                'distance': distance,
                'speed': speed,
                'current_distance': 0,
                'size': size,
                'color': color,
                'type': particle_type,
                'life': 1.0
            })
    
    def update_reality_particles(self):
        """Update reality change particles"""
        for particle in self.particles[:]:
            # Update position
            particle['current_distance'] += particle['speed']
            ratio = min(particle['current_distance'] / particle['distance'], 1.0)
            
            center_x, center_y = self.width // 2, self.height // 2
            angle = particle['angle']
            distance = particle['current_distance']
            
            x = center_x + math.cos(angle) * distance
            y = center_y + math.sin(angle) * distance
            particle['pos'] = (x, y)
            
            # Fade out when reaching target distance
            if ratio >= 0.8:
                particle['life'] -= 0.05
                if particle['life'] <= 0:
                    self.particles.remove(particle)
    
    def draw_cosmic_background(self):
        # Create a dark gradient background
        for y in range(0, self.height, 2):  # Step by 2 for performance
            # Calculate gradient colors
            gradient_factor = y / self.height
            r = int(5 + 10 * gradient_factor)
            g = int(8 + 2 * gradient_factor)
            b = int(25 + 5 * gradient_factor)
            
            # Draw a line with the calculated color
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y), 2)
    
    def draw_stars(self):
        for star in self.stars:
            x, y = star['pos']
            size = star['size']
            color = star['color']
            pygame.gfxdraw.filled_circle(self.screen, int(x), int(y), int(size), color)
    
    def draw_energy_particles(self):
        for particle in self.energy_particles:
            x, y = particle['pos']
            size = particle['size']
            base_color = particle['color']
            # Adjust alpha based on life
            alpha = int(255 * particle['life'])
            color = (*base_color[:3], alpha)
            
            # Draw particle with glow
            for i in range(3):
                glow_size = size * (3 - i) / 2
                glow_alpha = alpha // (i + 1)
                glow_color = (*base_color[:3], glow_alpha)
                pygame.gfxdraw.filled_circle(
                    self.screen, int(x), int(y), int(glow_size), glow_color
                )
    
    def draw_reality_particles(self):
        """Draw reality change particles"""
        for particle in self.particles:
            x, y = particle['pos']
            size = particle['size']
            base_color = particle['color']
            
            # Make particles glow
            alpha = int(255 * particle['life'])
            
            # Draw particle with glow
            for i in range(3):
                glow_size = size * (3 - i) / 1.5
                glow_alpha = alpha // (i + 1)
                glow_color = (*base_color[:3], glow_alpha)
                pygame.gfxdraw.filled_circle(
                    self.screen, int(x), int(y), int(glow_size), glow_color
                )
    
    def draw_main_interface(self):
        # Draw title
        title = self.font_large.render("Cosmic Reality Forge", True, self.colors['accent1'])
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw user info
        user_text = self.font_small.render(
            f"Reality Architect: {self.forge.username} | Cosmic Date: {self.forge.timestamp}", 
            True, (180, 180, 220)
        )
        self.screen.blit(user_text, (20, 20))
        
        # Draw current reality status
        current_rules = self.forge.current_rules
        status_text = self.font_medium.render("Current Reality Configuration", True, self.colors['accent2'])
        status_rect = status_text.get_rect(center=(self.width // 2, 120))
        self.screen.blit(status_text, status_rect)
        
        # Draw reality parameters in a circular pattern
        center_x, center_y = self.width // 2, self.height // 2 + 50
        radius = 200
        num_fields = len(asdict(current_rules))
        
        fields = list(asdict(current_rules).items())
        for i, (field, value) in enumerate(fields):
            angle = (i / num_fields) * 2 * math.pi
            
            # Calculate position
            node_x = center_x + radius * math.cos(angle)
            node_y = center_y + radius * math.sin(angle)
            
            # Animated glow effect
            pulse = 0.5 + 0.5 * math.sin(time.time() * 1.5 + i * 0.7)
            node_color = self.colors.get(field, self.colors['accent1'])
            
            # Adjust brightness based on pulse
            node_color = tuple(min(255, c + int(40 * pulse)) for c in node_color)
            
            # Draw node
            node_radius = 25 + 5 * pulse
            pygame.draw.circle(self.screen, node_color, (int(node_x), int(node_y)), int(node_radius))
            
            # Draw connecting line to center
            line_width = int(2 + 2 * pulse)
            line_alpha = int(100 + 50 * pulse)
            line_color = (*node_color[:3], line_alpha)
            
            # Draw semi-transparent line
            pygame.draw.line(
                self.screen, line_color, 
                (center_x, center_y), (node_x, node_y), 
                line_width
            )
            
            # Draw field name
            field_text = self.font_small.render(field.capitalize(), True, (255, 255, 255))
            field_rect = field_text.get_rect(center=(node_x, node_y - 40))
            self.screen.blit(field_text, field_rect)
            
            # Draw value
            value_text = self.font.render(value, True, (255, 255, 255))
            value_rect = value_text.get_rect(center=(node_x, node_y))
            self.screen.blit(value_text, value_rect)
        
        # Draw center node
        center_pulse = 0.5 + 0.5 * math.sin(time.time() * 2)
        center_radius = 50 + 10 * center_pulse
        
        # Multi-colored center node
        colors = [self.colors[field] for field in asdict(current_rules).keys()]
        
        # Create gradient effect
        for r in range(int(center_radius), 0, -5):
            color_idx = int((center_radius - r) / center_radius * len(colors))
            color_idx = min(color_idx, len(colors) - 1)
            color = colors[color_idx]
            
            # Add pulse effect
            color = tuple(min(255, c + int(30 * center_pulse)) for c in color)
            pygame.draw.circle(self.screen, color, (center_x, center_y), r)
        
        # Draw buttons
        button_y = self.height - 100
        
        # Edit button
        edit_rect = pygame.Rect(self.width // 2 - 350, button_y, 200, 60)
        pygame.draw.rect(self.screen, self.colors['button'], edit_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], edit_rect, 2)
        
        edit_text = self.font.render("Edit Reality", True, self.colors['text'])
        edit_text_rect = edit_text.get_rect(center=edit_rect.center)
        self.screen.blit(edit_text, edit_text_rect)
        
        # Save button
        save_rect = pygame.Rect(self.width // 2 - 100, button_y, 200, 60)
        pygame.draw.rect(self.screen, self.colors['button'], save_rect)
        pygame.draw.rect(self.screen, self.colors['success'], save_rect, 2)
        
        save_text = self.font.render("Save Reality", True, self.colors['text'])
        save_text_rect = save_text.get_rect(center=save_rect.center)
        self.screen.blit(save_text, save_text_rect)
        
        # Load button
        load_rect = pygame.Rect(self.width // 2 + 150, button_y, 200, 60)
        pygame.draw.rect(self.screen, self.colors['button'], load_rect)
        pygame.draw.rect(self.screen, self.colors['accent2'], load_rect, 2)
        
        load_text = self.font.render("Load Reality", True, self.colors['text'])
        load_text_rect = load_text.get_rect(center=load_rect.center)
        self.screen.blit(load_text, load_text_rect)
    
    def draw_edit_interface(self):
        # Draw title
        title = self.font_large.render("Edit Reality Parameters", True, self.colors['accent1'])
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['button'], back_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], back_rect, 2)
        
        back_text = self.font_small.render("Back", True, self.colors['text'])
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Draw parameter editing interface
        fields = list(asdict(self.forge.current_rules).items())
        param_y = 120
        param_height = 80
        
        for i, (field, current_value) in enumerate(fields):
            field_color = self.colors.get(field, self.colors['accent1'])
            field_rect = pygame.Rect(self.width // 2 - 400, param_y + i * param_height, 800, 60)
            
            # Determine if this field is being edited
            is_active = self.editing_field == field
            border_color = field_color if is_active else self.colors['highlight']
            border_width = 3 if is_active else 1
            
            # Draw field background with slight animation
            pulse = 0.5 + 0.5 * math.sin(time.time() * 1.5 + i * 0.3)
            bg_color = (
                int(30 + 15 * pulse if is_active else 20),
                int(30 + 15 * pulse if is_active else 20),
                int(50 + 15 * pulse if is_active else 40)
            )
            
            pygame.draw.rect(self.screen, bg_color, field_rect)
            pygame.draw.rect(self.screen, border_color, field_rect, border_width)
            
            # Draw field name
            name_text = self.font.render(field.capitalize(), True, field_color)
            self.screen.blit(name_text, (field_rect.x + 20, field_rect.y + 15))
            
            # Draw value options
            option_width = 120
            option_spacing = 10
            options_start_x = field_rect.x + 180
            
            for j, option in enumerate(self.field_options.get(field, [])):
                option_x = options_start_x + j * (option_width + option_spacing)
                option_rect = pygame.Rect(option_x, field_rect.y + 10, option_width, 40)
                
                # Highlight current value
                is_selected = option == current_value
                option_bg_color = field_color if is_selected else self.colors['button']
                text_color = (0, 0, 0) if is_selected else self.colors['text']
                
                pygame.draw.rect(self.screen, option_bg_color, option_rect, border_radius=5)
                
                # Draw option text
                option_text = self.font_small.render(option, True, text_color)
                option_text_rect = option_text.get_rect(center=option_rect.center)
                self.screen.blit(option_text, option_text_rect)
        
        # Apply button
        apply_rect = pygame.Rect(self.width // 2 - 100, param_y + len(fields) * param_height + 20, 200, 60)
        pygame.draw.rect(self.screen, (30, 100, 50), apply_rect)
        pygame.draw.rect(self.screen, (100, 200, 120), apply_rect, 2)
        
        apply_text = self.font.render("Apply Changes", True, (220, 255, 220))
        apply_text_rect = apply_text.get_rect(center=apply_rect.center)
        self.screen.blit(apply_text, apply_text_rect)
    
    def draw_saved_realities(self):
        # Draw title
        title = self.font_large.render("Saved Reality Configurations", True, self.colors['accent1'])
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['button'], back_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], back_rect, 2)
        
        back_text = self.font_small.render("Back", True, self.colors['text'])
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Draw saved realities
        saved = self.forge.saved_realities
        
        if not saved:
            # No saved realities message
            msg = self.font.render("No saved reality configurations found.", True, self.colors['text'])
            msg_rect = msg.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(msg, msg_rect)
            
            help_msg = self.font.render("Edit reality parameters and save them to build your library.", 
                                      True, self.colors['text'])
            help_rect = help_msg.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(help_msg, help_rect)
        else:
            # Draw saved reality list
            start_y = 120
            item_height = 120
            
            for i, reality in enumerate(saved):
                rect = pygame.Rect(self.width // 2 - 400, start_y + i * item_height, 800, item_height - 20)
                
                # Animated highlight for items
                pulse = 0.5 + 0.5 * math.sin(time.time() * 1.0 + i * 0.3)
                item_color = (
                    int(20 + 10 * pulse),
                    int(20 + 10 * pulse),
                    int(40 + 10 * pulse)
                )
                
                pygame.draw.rect(self.screen, item_color, rect)
                pygame.draw.rect(self.screen, self.colors['highlight'], rect, 2)
                
                # Name and timestamp
                name = reality.get("name", "Unnamed Reality")
                name_text = self.font_medium.render(name, True, self.colors['accent1'])
                self.screen.blit(name_text, (rect.x + 20, rect.y + 15))
                
                date_text = self.font_small.render(
                    f"Created: {reality.get('timestamp', 'Unknown')} by {reality.get('created_by', 'Unknown')}", 
                    True, self.colors['accent2']
                )
                self.screen.blit(date_text, (rect.x + 20, rect.y + 50))
                
                # Description
                desc = reality.get("description", "No description.")
                desc_text = self.font_small.render(desc[:80] + "..." if len(desc) > 80 else desc, True, self.colors['text'])
                self.screen.blit(desc_text, (rect.x + 20, rect.y + 75))
                
                # Apply button
                apply_rect = pygame.Rect(rect.right - 120, rect.y + 15, 100, 40)
                pygame.draw.rect(self.screen, (30, 100, 50), apply_rect)
                pygame.draw.rect(self.screen, (100, 200, 120), apply_rect, 2)
                
                apply_text = self.font_small.render("Apply", True, (220, 255, 220))
                apply_text_rect = apply_text.get_rect(center=apply_rect.center)
                self.screen.blit(apply_text, apply_text_rect)
                
                # View button
                view_rect = pygame.Rect(rect.right - 120, rect.y + 65, 100, 40)
                pygame.draw.rect(self.screen, (40, 60, 100), view_rect)
                pygame.draw.rect(self.screen, self.colors['accent2'], view_rect, 2)
                
                view_text = self.font_small.render("View", True, self.colors['text'])
                view_text_rect = view_text.get_rect(center=view_rect.center)
                self.screen.blit(view_text, view_text_rect)
    
    def draw_save_interface(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 220))
        self.screen.blit(overlay, (0, 0))
        
        # Create panel
        panel_rect = pygame.Rect(self.width // 2 - 350, self.height // 2 - 200, 700, 400)
        pygame.draw.rect(self.screen, self.colors['panel'], panel_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], panel_rect, 3)
        
        # Title
        title = self.font_large.render("Save Reality Configuration", True, self.colors['accent1'])
        title_rect = title.get_rect(center=(panel_rect.centerx, panel_rect.y + 40))
        self.screen.blit(title, title_rect)
        
        # Name input
        name_label = self.font.render("Name:", True, self.colors['text'])
        self.screen.blit(name_label, (panel_rect.x + 50, panel_rect.y + 100))
        
        name_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 130, panel_rect.width - 100, 50)
        pygame.draw.rect(self.screen, (40, 40, 60), name_rect)
        border_color = self.colors['accent1'] if self.save_field == "name" else self.colors['highlight']
        pygame.draw.rect(self.screen, border_color, name_rect, 2)
        
        name_text = self.font.render(self.save_name, True, self.colors['text'])
        self.screen.blit(name_text, (name_rect.x + 20, name_rect.y + 15))
        
        # Description input
        desc_label = self.font.render("Description:", True, self.colors['text'])
        self.screen.blit(desc_label, (panel_rect.x + 50, panel_rect.y + 200))
        
        desc_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 230, panel_rect.width - 100, 80)
        pygame.draw.rect(self.screen, (40, 40, 60), desc_rect)
        border_color = self.colors['accent1'] if self.save_field == "description" else self.colors['highlight']
        pygame.draw.rect(self.screen, border_color, desc_rect, 2)
        
        # Wrap description text across multiple lines
        if self.save_description:
            wrapped_text = [self.save_description[i:i+50] for i in range(0, len(self.save_description), 50)]
            for i, line in enumerate(wrapped_text[:2]):  # Show up to 2 lines
                line_text = self.font.render(line, True, self.colors['text'])
                self.screen.blit(line_text, (desc_rect.x + 20, desc_rect.y + 15 + i * 30))
        
        # Buttons
        save_rect = pygame.Rect(panel_rect.x + 150, panel_rect.y + 330, 180, 50)
        pygame.draw.rect(self.screen, (30, 100, 50), save_rect)
        pygame.draw.rect(self.screen, (100, 200, 120), save_rect, 2)
        
        save_text = self.font.render("Save", True, (220, 255, 220))
        save_text_rect = save_text.get_rect(center=save_rect.center)
        self.screen.blit(save_text, save_text_rect)
        
        cancel_rect = pygame.Rect(panel_rect.x + 370, panel_rect.y + 330, 180, 50)
        pygame.draw.rect(self.screen, (100, 30, 50), cancel_rect)
        pygame.draw.rect(self.screen, (200, 100, 120), cancel_rect, 2)
        
        cancel_text = self.font.render("Cancel", True, (255, 220, 220))
        cancel_text_rect = cancel_text.get_rect(center=cancel_rect.center)
        self.screen.blit(cancel_text, cancel_text_rect)
        
        # Blinking cursor for active input
        if time.time() % 1 > 0.5:
            cursor_pos = None
            if self.save_field == "name":
                text_width = name_text.get_width()
                cursor_pos = (name_rect.x + 20 + text_width, name_rect.y + 15)
                cursor_height = 30
            elif self.save_field == "description":
                # Position cursor at end of last line of text
                lines = [self.save_description[i:i+50] for i in range(0, len(self.save_description), 50)]
                if lines:
                    last_line = lines[-1]
                    line_surf = self.font.render(last_line, True, self.colors['text'])
                    line_index = min(len(lines) - 1, 1)  # Only show up to 2 lines
                    cursor_pos = (
                        desc_rect.x + 20 + line_surf.get_width(), 
                        desc_rect.y + 15 + line_index * 30
                    )
                    cursor_height = 30
                else:
                    cursor_pos = (desc_rect.x + 20, desc_rect.y + 15)
                    cursor_height = 30
                
            if cursor_pos:
                pygame.draw.line(
                    self.screen, self.colors['text'],
                    cursor_pos,
                    (cursor_pos[0], cursor_pos[1] + cursor_height),
                    2
                )
    
    def draw_reality_detail(self):
        if not self.selected_reality:
            self.active_view = "saved"
            return
        
        # Draw title
        title = self.font_large.render("Reality Configuration Details", True, self.colors['accent1'])
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['button'], back_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], back_rect, 2)
        
        back_text = self.font_small.render("Back", True, self.colors['text'])
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Reality name
        name_text = self.font_medium.render(self.selected_reality.get("name", "Unnamed Reality"), True, self.colors['accent1'])
        name_rect = name_text.get_rect(centerx=self.width // 2, top=120)
        self.screen.blit(name_text, name_rect)
        
        # Metadata
        metadata = self.font_small.render(
            f"Created: {self.selected_reality.get('timestamp', 'Unknown')} by {self.selected_reality.get('created_by', 'Unknown')}", 
            True, self.colors['accent2']
        )
        metadata_rect = metadata.get_rect(centerx=self.width // 2, top=160)
        self.screen.blit(metadata, metadata_rect)
        
        # Description
        desc = self.selected_reality.get("description", "No description provided.")
        desc_text = self.font.render(desc, True, self.colors['text'])
        desc_rect = desc_text.get_rect(centerx=self.width // 2, top=190)
        self.screen.blit(desc_text, desc_rect)
        
        # Draw reality parameters in a circular pattern
        center_x, center_y = self.width // 2, self.height // 2 + 70
        radius = 180
        rules = self.selected_reality.get("rules", {})
        num_fields = len(rules)
        
        fields = list(rules.items())
        for i, (field, value) in enumerate(fields):
            angle = (i / num_fields) * 2 * math.pi
            
            # Calculate position
            node_x = center_x + radius * math.cos(angle)
            node_y = center_y + radius * math.sin(angle)
            
            # Animated glow effect
            pulse = 0.5 + 0.5 * math.sin(time.time() * 1.5 + i * 0.7)
            node_color = self.colors.get(field, self.colors['accent1'])
            
            # Adjust brightness based on pulse
            node_color = tuple(min(255, c + int(40 * pulse)) for c in node_color)
            
            # Draw node
            node_radius = 25 + 5 * pulse
            pygame.draw.circle(self.screen, node_color, (int(node_x), int(node_y)), int(node_radius))
            
            # Draw connecting line to center
            line_width = int(2 + 2 * pulse)
            pygame.draw.line(
                self.screen, node_color, 
                (center_x, center_y), (node_x, node_y), 
                line_width
            )
            
            # Draw field name
            field_text = self.font_small.render(field.capitalize(), True, (255, 255, 255))
            field_rect = field_text.get_rect(center=(node_x, node_y - 40))
            self.screen.blit(field_text, field_rect)
            
            # Draw value
            value_text = self.font.render(value, True, (255, 255, 255))
            value_rect = value_text.get_rect(center=(node_x, node_y))
            self.screen.blit(value_text, value_rect)
        
        # Draw center node
        center_pulse = 0.5 + 0.5 * math.sin(time.time() * 2)
        center_radius = 40 + 10 * center_pulse
        
        # Multi-colored center node
        colors = [self.colors[field] for field in rules.keys() if field in self.colors]
        if not colors:
            colors = [self.colors['accent1']]
            
        # Create gradient effect
        for r in range(int(center_radius), 0, -5):
            color_idx = int((center_radius - r) / center_radius * len(colors))
            color_idx = min(color_idx, len(colors) - 1)
            color = colors[color_idx]
            
            # Add pulse effect
            color = tuple(min(255, c + int(30 * center_pulse)) for c in color)
            pygame.draw.circle(self.screen, color, (center_x, center_y), r)
        
        # Apply button
        apply_rect = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 60)
        pygame.draw.rect(self.screen, (30, 100, 50), apply_rect)
        pygame.draw.rect(self.screen, (100, 200, 120), apply_rect, 2)
        
        apply_text = self.font.render("Apply Reality", True, (220, 255, 220))
        apply_text_rect = apply_text.get_rect(center=apply_rect.center)
        self.screen.blit(apply_text, apply_text_rect)
    
    def draw_notification(self):
        if self.notification and time.time() < self.notification_timer:
            # Calculate fade out
            time_left = self.notification_timer - time.time()
            alpha = min(255, int(time_left * 255))
            
            # Create notification surface
            notification_surf = self.font.render(self.notification[0], True, self.notification[1])
            notification_rect = notification_surf.get_rect(center=(self.width // 2, self.height - 50))
            
            # Draw background
            bg_rect = notification_rect.inflate(40, 20)
            bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surf.fill((20, 20, 40, alpha))
            self.screen.blit(bg_surf, bg_rect)
            
            # Draw text with alpha
            text_surf = pygame.Surface(notification_surf.get_size(), pygame.SRCALPHA)
            text_surf.blit(notification_surf, (0, 0))
            text_surf.set_alpha(alpha)
            self.screen.blit(text_surf, notification_rect)
    
    def show_notification(self, message, color=(220, 220, 255), duration=3):
        self.notification = (message, color)
        self.notification_timer = time.time() + duration
    
    def handle_click(self, pos):
        if self.save_mode:
            # Handle save interface clicks
            panel_rect = pygame.Rect(self.width // 2 - 350, self.height // 2 - 200, 700, 400)
            
            # Name input
            name_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 130, panel_rect.width - 100, 50)
            if name_rect.collidepoint(pos):
                self.save_field = "name"
                return
            
            # Description input
            desc_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 230, panel_rect.width - 100, 80)
            if desc_rect.collidepoint(pos):
                self.save_field = "description"
                return
            
            # Save button
            save_rect = pygame.Rect(panel_rect.x + 150, panel_rect.y + 330, 180, 50)
            if save_rect.collidepoint(pos):
                if not self.save_name.strip():
                    self.show_notification("Please enter a name for this reality configuration", self.colors['warning'])
                    return
                
                # Save the reality
                result = self.forge.save_reality(self.save_name, self.save_description)
                self.show_notification("Reality configuration saved successfully", self.colors['success'])
                self.save_mode = False
                return
            
            # Cancel button
            cancel_rect = pygame.Rect(panel_rect.x + 370, panel_rect.y + 330, 180, 50)
            if cancel_rect.collidepoint(pos):
                self.save_mode = False
                return
            
            return
        
        if self.active_view == "main":
            # Edit button
            edit_rect = pygame.Rect(self.width // 2 - 350, self.height - 100, 200, 60)
            if edit_rect.collidepoint(pos):
                self.active_view = "edit"
                return
            
            # Save button
            save_rect = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 60)
            if save_rect.collidepoint(pos):
                self.save_mode = True
                self.save_name = ""
                self.save_description = ""
                self.save_field = "name"
                return
            
            # Load button
            load_rect = pygame.Rect(self.width // 2 + 150, self.height - 100, 200, 60)
            if load_rect.collidepoint(pos):
                self.active_view = "saved"
                self.forge.load_saved_realities()  # Refresh the list
                return
        
        elif self.active_view == "edit":
            # Back button
            back_rect = pygame.Rect(20, 20, 100, 40)
            if back_rect.collidepoint(pos):
                self.active_view = "main"
                self.editing_field = None
                return
            
            # Check for parameter field clicks
            fields = list(asdict(self.forge.current_rules).items())
            param_y = 120
            param_height = 80
            
            for i, (field, current_value) in enumerate(fields):
                field_rect = pygame.Rect(self.width // 2 - 400, param_y + i * param_height, 800, 60)
                
                if field_rect.collidepoint(pos):
                    # Check if clicked on one of the options
                    options = self.field_options.get(field, [])
                    option_width = 120
                    option_spacing = 10
                    options_start_x = field_rect.x + 180
                    
                    for j, option in enumerate(options):
                        option_x = options_start_x + j * (option_width + option_spacing)
                        option_rect = pygame.Rect(option_x, field_rect.y + 10, option_width, 40)
                        
                        if option_rect.collidepoint(pos):
                            # Update the field to this option
                            setattr(self.forge.current_rules, field, option)
                            self.show_notification(f"Updated {field} to {option}", self.colors[field])
                            return
            
            # Apply button
            apply_rect = pygame.Rect(self.width // 2 - 100, param_y + len(fields) * param_height + 20, 200, 60)
            if apply_rect.collidepoint(pos):
                # Apply changes and show reality change animation
                self.create_reality_change_particles()
                self.show_notification("Reality parameters updated", self.colors['success'])
                self.active_view = "main"
                return
        
        elif self.active_view == "saved":
            # Back button
            back_rect = pygame.Rect(20, 20, 100, 40)
            if back_rect.collidepoint(pos):
                self.active_view = "main"
                return
            
            # Check for saved reality clicks
            saved = self.forge.saved_realities
            start_y = 120
            item_height = 120
            
            for i, reality in enumerate(saved):
                rect = pygame.Rect(self.width // 2 - 400, start_y + i * item_height, 800, item_height - 20)
                
                # Apply button
                apply_rect = pygame.Rect(rect.right - 120, rect.y + 15, 100, 40)
                if apply_rect.collidepoint(pos):
                    # Apply this reality
                    result = self.forge.apply_saved_reality(reality.get("id"))
                    if result["status"] == "reality_updated":
                        self.create_reality_change_particles()
                        self.show_notification(f"Applied reality: {reality.get('name')}", self.colors['success'])
                        self.active_view = "main"
                    else:
                        self.show_notification("Failed to apply reality configuration", self.colors['warning'])
                    return
                
                # View button
                view_rect = pygame.Rect(rect.right - 120, rect.y + 65, 100, 40)
                if view_rect.collidepoint(pos):
                    # View reality details
                    self.selected_reality = reality
                    self.active_view = "detail"
                    return
        
        elif self.active_view == "detail":
            # Back button
            back_rect = pygame.Rect(20, 20, 100, 40)
            if back_rect.collidepoint(pos):
                self.active_view = "saved"
                return
            
            # Apply button
            apply_rect = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 60)
            if apply_rect.collidepoint(pos):
                # Apply this reality
                result = self.forge.apply_saved_reality(self.selected_reality.get("id"))
                if result["status"] == "reality_updated":
                    self.create_reality_change_particles()
                    self.show_notification(f"Applied reality: {self.selected_reality.get('name')}", self.colors['success'])
                    self.active_view = "main"
                else:
                    self.show_notification("Failed to apply reality configuration", self.colors['warning'])
                return
    
    def handle_key(self, key, unicode):
        if self.save_mode:
            if key == pygame.K_ESCAPE:
                self.save_mode = False
                return
            
            if key == pygame.K_TAB:
                self.save_field = "description" if self.save_field == "name" else "name"
                return
            
            if key == pygame.K_RETURN:
                if self.save_field == "name":
                    self.save_field = "description"
                elif not self.save_name.strip():
                    self.show_notification("Please enter a name for this reality configuration", self.colors['warning'])
                else:
                    # Save the reality
                    result = self.forge.save_reality(self.save_name, self.save_description)
                    self.show_notification("Reality configuration saved successfully", self.colors['success'])
                    self.save_mode = False
                return
            
            if key == pygame.K_BACKSPACE:
                if self.save_field == "name":
                    self.save_name = self.save_name[:-1]
                else:
                    self.save_description = self.save_description[:-1]
                return
            
            # Regular text input
            if self.save_field == "name":
                self.save_name += unicode
            else:
                self.save_description += unicode
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not self.save_mode:
                        if self.active_view != "main":
                            self.active_view = "main"
                        else:
                            self.running = False
                    else:
                        self.handle_key(event.key, event.unicode)
            
            # Update elements
            self.update_stars()
            self.update_energy_particles()
            self.update_reality_particles()
            
            # Draw everything
            self.draw_cosmic_background()
            self.draw_stars()
            self.draw_energy_particles()
            
            # Draw the appropriate interface
            if self.active_view == "main":
                self.draw_main_interface()
            elif self.active_view == "edit":
                self.draw_edit_interface()
            elif self.active_view == "saved":
                self.draw_saved_realities()
            elif self.active_view == "detail":
                self.draw_reality_detail()
            
            # Draw reality change particles
            self.draw_reality_particles()
            
            # Draw save interface if active
            if self.save_mode:
                self.draw_save_interface()
            
            # Draw notifications
            self.draw_notification()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

# Helper function to initialize with sample data
def initialize_sample_realities():
    """Create some sample reality configurations"""
    forge = RealityForge(username="behicof", timestamp="2025-04-17 14:01:33")
    
    # Sample 1: Quantum Reality
    forge.rewrite_rules({
        "value": "quantum",
        "time": "branching",
        "risk": "probability-based",
        "dimension": "5D",
        "causality": "non-linear",
        "probability": "multiversal",
        "observer": "quantum"
    })
    forge.save_reality(
        "Quantum Reality", 
        "A reality where all possibilities exist simultaneously until observed."
    )
    
    # Sample 2: Stable Prosperity
    forge.rewrite_rules({
        "value": "static",
        "time": "linear",
        "risk": "eliminated",
        "dimension": "3D",
        "causality": "forward",
        "probability": "deterministic",
        "observer": "conscious"
    })
    forge.save_reality(
        "Stable Prosperity", 
        "A reality of consistent growth and eliminated financial risk."
    )
    
    # Sample 3: Cyclical Abundance
    forge.rewrite_rules({
        "value": "cyclical",
        "time": "cyclical",
        "risk": "reverse-correlated",
        "dimension": "4D",
        "causality": "bidirectional",
        "probability": "wave-based",
        "observer": "collective"
    })
    forge.save_reality(
        "Cyclical Abundance", 
        "A reality where value flows in harmonious cycles with predictable patterns."
    )
    
    # Reset to default
    forge.rewrite_rules({
        "value": "dynamic",
        "time": "linear",
        "risk": "real",
        "dimension": "3D",
        "causality": "forward",
        "probability": "quantum",
        "observer": "conscious"
    })
    
    return forge

if __name__ == "__main__":
    # Initialize with sample data
    forge = initialize_sample_realities()
    
    # Run the visualizer
    app = CosmicRealityVisualizer(forge)
    app.show_notification("Welcome to the Cosmic Reality Forge", (180, 220, 255), 5)
    app.run()