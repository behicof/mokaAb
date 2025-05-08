import pygame
import random
import math
import json
import os
from pygame import gfxdraw
import time
from datetime import datetime

class CosmicLibrary:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cosmic Library - Akashic Records")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.font_small = pygame.font.SysFont('Arial', 16)
        self.font = pygame.font.SysFont('Arial', 24)
        self.font_large = pygame.font.SysFont('Arial', 36)
        
        # Library data
        self.library_path = "cosmic_data"
        self.ensure_library_exists()
        self.categories = [
            "Universal Knowledge",
            "Cosmic Events",
            "Soul Records",
            "Planetary Wisdom",
            "Consciousness Patterns",
            "Vibrational Data",
            "Timeline Recordings"
        ]
        
        # Visual elements
        self.stars = []
        self.create_stars(300)
        
        # UI state
        self.active_category = None
        self.viewing_records = False
        self.records = []
        self.input_active = False
        self.input_text = ""
        self.input_title = ""
        self.message = ""
        self.message_timer = 0
        
        # User info
        self.username = "behicof"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def ensure_library_exists(self):
        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path)
            
        # Create category folders
        for category in self.categories:
            category_path = os.path.join(self.library_path, category.replace(" ", "_"))
            if not os.path.exists(category_path):
                os.makedirs(category_path)
    
    def create_stars(self, count):
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
    
    def update_stars(self):
        for star in self.stars:
            # Make stars twinkle
            brightness = 150 + 105 * math.sin(time.time() * star['twinkle_rate'] * 10)
            star['color'] = (brightness, brightness, brightness)
    
    def draw_cosmic_background(self):
        # Create a dark gradient background
        for y in range(self.height):
            # Calculate gradient colors
            gradient_factor = y / self.height
            r = int(5 + 20 * gradient_factor)
            g = int(5 + 10 * gradient_factor)
            b = int(30 + 20 * gradient_factor)
            
            # Draw a line with the calculated color
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
    
    def draw_stars(self):
        for star in self.stars:
            x, y = star['pos']
            size = star['size']
            color = star['color']
            pygame.gfxdraw.filled_circle(self.screen, int(x), int(y), int(size), color)
    
    def draw_library_interface(self):
        if self.input_active:
            self.draw_input_interface()
            return
            
        if self.active_category and self.viewing_records:
            self.draw_records_view()
            return
            
        # Draw title
        title = self.font_large.render("Cosmic Library - Akashic Records", True, (220, 220, 255))
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw user info
        user_text = self.font_small.render(f"User: {self.username} | {self.timestamp}", 
                                          True, (180, 180, 220))
        self.screen.blit(user_text, (20, 20))
        
        # Draw categories
        category_height = 80
        start_y = 150
        for i, category in enumerate(self.categories):
            # Calculate position
            rect = pygame.Rect(self.width // 2 - 200, start_y + i * category_height, 400, 60)
            
            # Draw glowing box
            glow_factor = 0.5 + 0.5 * math.sin(time.time() * 2 + i * 0.5)
            glow_color = (
                int(40 + 40 * glow_factor),
                int(20 + 30 * glow_factor),
                int(80 + 50 * glow_factor)
            )
            pygame.draw.rect(self.screen, glow_color, rect)
            pygame.draw.rect(self.screen, (100, 100, 180), rect, 2)
            
            # Draw category name
            text = self.font.render(category, True, (220, 220, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        
        # Draw add new record button
        add_rect = pygame.Rect(self.width // 2 - 150, start_y + len(self.categories) * category_height + 20, 300, 60)
        pygame.draw.rect(self.screen, (30, 100, 50), add_rect)
        pygame.draw.rect(self.screen, (100, 200, 120), add_rect, 2)
        
        add_text = self.font.render("Add New Cosmic Record", True, (220, 255, 220))
        add_text_rect = add_text.get_rect(center=add_rect.center)
        self.screen.blit(add_text, add_text_rect)
        
        # Draw message if exists
        if self.message and time.time() < self.message_timer:
            msg = self.font.render(self.message, True, (255, 220, 150))
            msg_rect = msg.get_rect(center=(self.width // 2, self.height - 40))
            self.screen.blit(msg, msg_rect)
    
    def draw_records_view(self):
        # Draw back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, (60, 60, 100), back_rect)
        pygame.draw.rect(self.screen, (120, 120, 180), back_rect, 2)
        
        back_text = self.font_small.render("Back", True, (220, 220, 255))
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Draw category title
        title = self.font_large.render(self.active_category, True, (220, 220, 255))
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw records
        if not self.records:
            # No records message
            msg = self.font.render("No cosmic records found in this category.", True, (180, 180, 220))
            msg_rect = msg.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(msg, msg_rect)
            
            add_msg = self.font.render("Add new records to begin collecting cosmic knowledge.", 
                                      True, (180, 180, 220))
            add_msg_rect = add_msg.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(add_msg, add_msg_rect)
        else:
            # Draw scrollable record list
            start_y = 120
            record_height = 100
            
            for i, record in enumerate(self.records):
                # Record container
                rect = pygame.Rect(self.width // 2 - 300, start_y + i * record_height, 600, 80)
                pygame.draw.rect(self.screen, (40, 40, 70), rect)
                pygame.draw.rect(self.screen, (100, 100, 180), rect, 2)
                
                # Title
                title = self.font.render(record["title"], True, (220, 220, 255))
                self.screen.blit(title, (rect.x + 20, rect.y + 10))
                
                # Preview text (truncated)
                preview = record["content"][:50] + "..." if len(record["content"]) > 50 else record["content"]
                text = self.font_small.render(preview, True, (180, 180, 220))
                self.screen.blit(text, (rect.x + 20, rect.y + 40))
                
                # Date
                date = self.font_small.render(record["date"], True, (150, 150, 200))
                date_rect = date.get_rect(right=rect.right - 20, centery=rect.y + 20)
                self.screen.blit(date, date_rect)
    
    def draw_input_interface(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Draw input panel
        panel_rect = pygame.Rect(self.width // 2 - 350, self.height // 2 - 200, 700, 400)
        pygame.draw.rect(self.screen, (30, 30, 60), panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 180), panel_rect, 3)
        
        # Title
        title = self.font_large.render("Add Cosmic Knowledge", True, (220, 220, 255))
        title_rect = title.get_rect(center=(self.width // 2, panel_rect.y + 40))
        self.screen.blit(title, title_rect)
        
        # Input fields
        title_label = self.font.render("Title:", True, (200, 200, 240))
        self.screen.blit(title_label, (panel_rect.x + 30, panel_rect.y + 100))
        
        title_input_rect = pygame.Rect(panel_rect.x + 30, panel_rect.y + 130, 640, 40)
        pygame.draw.rect(self.screen, (50, 50, 80), title_input_rect)
        pygame.draw.rect(self.screen, (120, 120, 200), title_input_rect, 2)
        
        title_text = self.font.render(self.input_title, True, (220, 220, 255))
        self.screen.blit(title_text, (title_input_rect.x + 10, title_input_rect.y + 10))
        
        # Content field
        content_label = self.font.render("Cosmic Information:", True, (200, 200, 240))
        self.screen.blit(content_label, (panel_rect.x + 30, panel_rect.y + 180))
        
        content_input_rect = pygame.Rect(panel_rect.x + 30, panel_rect.y + 210, 640, 100)
        pygame.draw.rect(self.screen, (50, 50, 80), content_input_rect)
        pygame.draw.rect(self.screen, (120, 120, 200), content_input_rect, 2)
        
        # Render multiline text
        y_offset = 0
        for line in self.input_text.split('\n'):
            if y_offset < 80:  # Stop rendering if we're out of the box
                text = self.font.render(line, True, (220, 220, 255))
                self.screen.blit(text, (content_input_rect.x + 10, content_input_rect.y + 10 + y_offset))
                y_offset += 25
        
        # Buttons
        save_rect = pygame.Rect(panel_rect.x + 150, panel_rect.y + 330, 180, 50)
        pygame.draw.rect(self.screen, (30, 100, 50), save_rect)
        pygame.draw.rect(self.screen, (100, 200, 120), save_rect, 2)
        
        save_text = self.font.render("Save Record", True, (220, 255, 220))
        save_text_rect = save_text.get_rect(center=save_rect.center)
        self.screen.blit(save_text, save_text_rect)
        
        cancel_rect = pygame.Rect(panel_rect.x + 370, panel_rect.y + 330, 180, 50)
        pygame.draw.rect(self.screen, (100, 30, 50), cancel_rect)
        pygame.draw.rect(self.screen, (200, 100, 120), cancel_rect, 2)
        
        cancel_text = self.font.render("Cancel", True, (255, 220, 220))
        cancel_text_rect = cancel_text.get_rect(center=cancel_rect.center)
        self.screen.blit(cancel_text, cancel_text_rect)
        
        # Category selection
        category_label = self.font.render("Category:", True, (200, 200, 240))
        self.screen.blit(category_label, (panel_rect.x + 150, panel_rect.y + 70))
        
        # Draw selected category
        if self.active_category:
            cat_text = self.font.render(self.active_category, True, (180, 220, 255))
            self.screen.blit(cat_text, (panel_rect.x + 250, panel_rect.y + 70))
            
    def save_record(self):
        if not self.input_title.strip() or not self.input_text.strip():
            self.message = "Please provide both title and content"
            self.message_timer = time.time() + 3
            return
            
        record = {
            "title": self.input_title,
            "content": self.input_text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": self.username
        }
        
        # Save to file
        category_folder = os.path.join(self.library_path, self.active_category.replace(" ", "_"))
        filename = os.path.join(category_folder, f"{int(time.time())}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
            
        self.message = "Cosmic knowledge recorded successfully"
        self.message_timer = time.time() + 3
        self.input_active = False
        self.load_records()
        
    def load_records(self):
        self.records = []
        if not self.active_category:
            return
            
        category_folder = os.path.join(self.library_path, self.active_category.replace(" ", "_"))
        if not os.path.exists(category_folder):
            return
            
        for filename in os.listdir(category_folder):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(category_folder, filename), 'r', encoding='utf-8') as f:
                        record = json.load(f)
                        self.records.append(record)
                except:
                    continue
                    
        # Sort by date (newest first)
        self.records.sort(key=lambda x: x.get("date", ""), reverse=True)
        
    def handle_click(self, pos):
        if self.input_active:
            # Input dialog buttons
            panel_rect = pygame.Rect(self.width // 2 - 350, self.height // 2 - 200, 700, 400)
            
            # Title input field
            title_input_rect = pygame.Rect(panel_rect.x + 30, panel_rect.y + 130, 640, 40)
            if title_input_rect.collidepoint(pos):
                self.input_mode = "title"
                
            # Content input field
            content_input_rect = pygame.Rect(panel_rect.x + 30, panel_rect.y + 210, 640, 100)
            if content_input_rect.collidepoint(pos):
                self.input_mode = "content"
                
            # Save button
            save_rect = pygame.Rect(panel_rect.x + 150, panel_rect.y + 330, 180, 50)
            if save_rect.collidepoint(pos):
                self.save_record()
                
            # Cancel button
            cancel_rect = pygame.Rect(panel_rect.x + 370, panel_rect.y + 330, 180, 50)
            if cancel_rect.collidepoint(pos):
                self.input_active = False
            
            return
            
        if self.active_category and self.viewing_records:
            # Back button
            back_rect = pygame.Rect(20, 20, 100, 40)
            if back_rect.collidepoint(pos):
                self.viewing_records = False
                self.active_category = None
                return
                
            # Check for record clicks
            start_y = 120
            record_height = 100
            
            for i, record in enumerate(self.records):
                rect = pygame.Rect(self.width // 2 - 300, start_y + i * record_height, 600, 80)
                if rect.collidepoint(pos):
                    # TODO: View full record
                    pass
                    
            return
            
        # Category selection
        category_height = 80
        start_y = 150
        for i, category in enumerate(self.categories):
            rect = pygame.Rect(self.width // 2 - 200, start_y + i * category_height, 400, 60)
            if rect.collidepoint(pos):
                self.active_category = category
                self.viewing_records = True
                self.load_records()
                return
                
        # Add new record button
        add_rect = pygame.Rect(self.width // 2 - 150, start_y + len(self.categories) * category_height + 20, 300, 60)
        if add_rect.collidepoint(pos):
            self.show_category_selection()
            
    def show_category_selection(self):
        # For simplicity, just pick the first category 
        # In a full implementation, you'd show a category selection dialog
        if not self.active_category:
            self.active_category = self.categories[0]
            
        self.input_active = True
        self.input_title = ""
        self.input_text = ""
        self.input_mode = "title"  # Start with title input
        
    def handle_key(self, key, unicode):
        if not self.input_active:
            return
            
        if key == pygame.K_ESCAPE:
            self.input_active = False
            return
            
        if key == pygame.K_TAB:
            self.input_mode = "content" if self.input_mode == "title" else "title"
            return
            
        if key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.save_record()
            return
            
        if key == pygame.K_BACKSPACE:
            if self.input_mode == "title":
                self.input_title = self.input_title[:-1]
            else:
                self.input_text = self.input_text[:-1]
            return
            
        # Regular text input
        if self.input_mode == "title":
            if key == pygame.K_RETURN:
                self.input_mode = "content"
            else:
                self.input_title += unicode
        else:
            if key == pygame.K_RETURN:
                self.input_text += "\n"
            else:
                self.input_text += unicode
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not self.input_active:
                        self.running = False
                    else:
                        self.handle_key(event.key, event.unicode)
            
            # Update and draw
            self.update_stars()
            self.draw_cosmic_background()
            self.draw_stars()
            self.draw_library_interface()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    app = CosmicLibrary()
    app.run()