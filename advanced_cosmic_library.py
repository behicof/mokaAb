import pygame
import random
import math
import json
import os
import time
from datetime import datetime
import textwrap

class AdvancedCosmicLibrary:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1280, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cosmic Akashic Records Library")
        self.clock = pygame.time.Clock()
        self.running = True
        
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
            'tag': (60, 80, 120)
        }
        
        # User info - provided by the user
        self.username = "behicof"
        self.timestamp = "2025-04-17 13:55:08"
        
        # Library data
        self.library_path = "cosmic_data"
        self.ensure_library_exists()
        self.categories = self.get_categories()
        self.total_records = self.count_total_records()
        
        # Visual elements
        self.stars = []
        self.energy_particles = []
        self.create_stars(300)
        self.create_energy_particles(50)
        
        # UI state
        self.active_category = None
        self.viewing_records = False
        self.viewing_record_detail = False
        self.current_record = None
        self.records = []
        self.search_results = []
        self.is_searching = False
        self.search_query = ""
        
        # Input state
        self.input_active = False
        self.input_mode = None
        self.input_title = ""
        self.input_content = ""
        self.input_tags = ""
        self.selected_category = None
        
        # Notification system
        self.notification = None
        self.notification_timer = 0
        
        # Scrolling
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Search
        self.search_active = False
        self.search_text = ""
        
        # Animation timers
        self.animation_time = 0
        
    def ensure_library_exists(self):
        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path)
    
    def get_categories(self):
        categories = []
        if os.path.exists(self.library_path):
            for item in os.listdir(self.library_path):
                item_path = os.path.join(self.library_path, item)
                if os.path.isdir(item_path):
                    categories.append(item.replace("_", " "))
        return sorted(categories)
    
    def count_total_records(self):
        total = 0
        for category in self.categories:
            category_folder = os.path.join(self.library_path, category.replace(" ", "_"))
            if os.path.exists(category_folder):
                total += len([f for f in os.listdir(category_folder) if f.endswith('.json')])
        return total
    
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
    
    def draw_main_interface(self):
        # Draw title
        title = self.font_large.render("Cosmic Akashic Records Library", True, self.colors['text'])
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw user info
        user_text = self.font_small.render(
            f"Librarian: {self.username} | Cosmic Date: {self.timestamp}", 
            True, (180, 180, 220)
        )
        self.screen.blit(user_text, (20, 20))
        
        # Draw record count
        record_text = self.font_small.render(
            f"Total Knowledge Records: {self.total_records}", 
            True, (180, 180, 220)
        )
        record_rect = record_text.get_rect(right=self.width - 20, top=20)
        self.screen.blit(record_text, record_rect)
        
        # Draw search button
        search_rect = pygame.Rect(self.width - 180, 60, 160, 40)
        pygame.draw.rect(self.screen, self.colors['button'], search_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], search_rect, 2)
        
        search_text = self.font.render("Search", True, self.colors['text'])
        search_text_rect = search_text.get_rect(center=search_rect.center)
        self.screen.blit(search_text, search_text_rect)
        
        # Draw categories
        subtitle = self.font_medium.render("Cosmic Knowledge Categories", True, self.colors['accent1'])
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 120))
        self.screen.blit(subtitle, subtitle_rect)
        
        category_height = 80
        start_y = 170
        col_width = self.width // 2 - 100
        
        for i, category in enumerate(self.categories):
            # Calculate position (2 columns)
            col = i % 2
            row = i // 2
            
            x = 100 + col * (col_width + 200)
            y = start_y + row * category_height
            
            rect = pygame.Rect(x, y, col_width, 60)
            
            # Calculate animation effect
            pulse = 0.5 + 0.5 * math.sin(time.time() * 1.5 + i * 0.7)
            glow_size = int(2 + 2 * pulse)
            
            # Draw glowing box with animation
            glow_color = (
                int(40 + 30 * pulse),
                int(20 + 30 * pulse),
                int(80 + 40 * pulse)
            )
            pygame.draw.rect(self.screen, glow_color, rect)
            pygame.draw.rect(self.screen, self.colors['highlight'], rect, glow_size)
            
            # Draw category name
            text = self.font.render(category, True, self.colors['text'])
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
            
            # Draw record count for this category
            count = self.count_records_in_category(category)
            count_text = self.font_small.render(f"{count} records", True, self.colors['accent2'])
            count_rect = count_text.get_rect(centerx=rect.centerx, top=rect.bottom + 5)
            self.screen.blit(count_text, count_rect)
        
        # Draw add new record button
        rows = (len(self.categories) + 1) // 2  # Calculate rows needed
        add_rect = pygame.Rect(self.width // 2 - 150, start_y + rows * category_height + 40, 300, 60)
        
        # Animated button glow
        pulse = 0.5 + 0.5 * math.sin(time.time() * 2)
        button_color = (
            int(30 + 20 * pulse),
            int(80 + 20 * pulse),
            int(50 + 20 * pulse)
        )
        
        pygame.draw.rect(self.screen, button_color, add_rect)
        pygame.draw.rect(self.screen, (100, 200, 120), add_rect, 2)
        
        add_text = self.font.render("Add New Cosmic Record", True, (220, 255, 220))
        add_text_rect = add_text.get_rect(center=add_rect.center)
        self.screen.blit(add_text, add_text_rect)
    
    def count_records_in_category(self, category):
        category_folder = os.path.join(self.library_path, category.replace(" ", "_"))
        if os.path.exists(category_folder):
            return len([f for f in os.listdir(category_folder) if f.endswith('.json')])
        return 0
    
    def draw_category_view(self):
        # Draw back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['button'], back_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], back_rect, 2)
        
        back_text = self.font_small.render("Back", True, self.colors['text'])
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Draw category title
        title = self.font_large.render(self.active_category, True, self.colors['accent1'])
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw add record button for this category
        add_rect = pygame.Rect(self.width - 220, 20, 200, 40)
        pygame.draw.rect(self.screen, self.colors['button'], add_rect)
        pygame.draw.rect(self.screen, (100, 200, 120), add_rect, 2)
        
        add_text = self.font_small.render("Add Record", True, (220, 255, 220))
        add_text_rect = add_text.get_rect(center=add_rect.center)
        self.screen.blit(add_text, add_text_rect)
        
        # Draw records
        if not self.records:
            # No records message
            msg = self.font.render("No cosmic records found in this category.", True, self.colors['text'])
            msg_rect = msg.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(msg, msg_rect)
            
            add_msg = self.font.render("Add new records to begin collecting cosmic knowledge.", 
                                      True, self.colors['text'])
            add_msg_rect = add_msg.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(add_msg, add_msg_rect)
        else:
            # Draw scrollable record list
            start_y = 120 - self.scroll_offset
            record_height = 140
            
            for i, record in enumerate(self.records):
                y_pos = start_y + i * record_height
                
                # Skip records that are off-screen
                if y_pos + record_height < 0 or y_pos > self.height:
                    continue
                
                # Record container
                rect = pygame.Rect(self.width // 2 - 400, y_pos, 800, record_height - 20)
                
                # Animated highlight for records
                pulse = 0.5 + 0.5 * math.sin(time.time() * 1.0 + i * 0.3)
                record_color = (
                    int(20 + 10 * pulse),
                    int(20 + 10 * pulse),
                    int(40 + 10 * pulse)
                )
                
                pygame.draw.rect(self.screen, record_color, rect)
                pygame.draw.rect(self.screen, self.colors['highlight'], rect, 2)
                
                # Title
                title = self.font_medium.render(record["title"], True, self.colors['accent1'])
                self.screen.blit(title, (rect.x + 20, rect.y + 15))
                
                # Preview text (truncated)
                preview = record["content"][:100] + "..." if len(record["content"]) > 100 else record["content"]
                text = self.font_small.render(preview, True, self.colors['text'])
                self.screen.blit(text, (rect.x + 20, rect.y + 55))
                
                # Date and user
                date_user = self.font_small.render(
                    f"Recorded: {record.get('date', 'Unknown')} by {record.get('user', 'Unknown')}", 
                    True, self.colors['accent2']
                )
                self.screen.blit(date_user, (rect.x + 20, rect.y + 85))
                
                # Tags
                if "tags" in record and record["tags"]:
                    tags_x = rect.x + 20
                    tags_y = rect.y + 110
                    
                    for tag in record["tags"][:5]:  # Display up to 5 tags
                        tag_surf = self.font_tiny.render(tag, True, (220, 220, 255))
                        tag_rect = tag_surf.get_rect(topleft=(tags_x, tags_y))
                        tag_bg = tag_rect.inflate(20, 10)
                        pygame.draw.rect(self.screen, self.colors['tag'], tag_bg, border_radius=10)
                        self.screen.blit(tag_surf, tag_rect)
                        tags_x += tag_bg.width + 10
                        
                        if tags_x > rect.right - 100:
                            break
            
            # Draw scrollbar if needed
            total_height = len(self.records) * record_height
            if total_height > self.height:
                self.max_scroll = total_height - self.height + 120
                
                scrollbar_height = min(self.height * self.height / total_height, self.height)
                scroll_ratio = self.scroll_offset / self.max_scroll if self.max_scroll > 0 else 0
                scrollbar_pos = scroll_ratio * (self.height - scrollbar_height)
                
                scrollbar_rect = pygame.Rect(
                    self.width - 20, scrollbar_pos, 
                    10, scrollbar_height
                )
                pygame.draw.rect(self.screen, self.colors['highlight'], scrollbar_rect)
            else:
                self.max_scroll = 0
    
    def draw_record_detail(self):
        if not self.current_record:
            self.viewing_record_detail = False
            return
            
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 220))
        self.screen.blit(overlay, (0, 0))
        
        # Create panel
        panel_rect = pygame.Rect(self.width // 2 - 450, 50, 900, self.height - 100)
        pygame.draw.rect(self.screen, self.colors['panel'], panel_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], panel_rect, 3)
        
        # Close button
        close_rect = pygame.Rect(panel_rect.right - 60, panel_rect.top + 20, 40, 40)
        pygame.draw.rect(self.screen, (100, 30, 30), close_rect)
        
        close_text = self.font_medium.render("×", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=close_rect.center)
        self.screen.blit(close_text, close_text_rect)
        
        # Title
        title = self.font_large.render(self.current_record["title"], True, self.colors['accent1'])
        title_rect = title.get_rect(topleft=(panel_rect.x + 30, panel_rect.y + 30))
        self.screen.blit(title, title_rect)
        
        # Metadata
        metadata = self.font_small.render(
            f"Category: {self.active_category} | "
            f"Recorded: {self.current_record.get('date', 'Unknown')} | "
            f"By: {self.current_record.get('user', 'Unknown')}", 
            True, self.colors['accent2']
        )
        metadata_rect = metadata.get_rect(topleft=(panel_rect.x + 30, panel_rect.y + 80))
        self.screen.blit(metadata, metadata_rect)
        
        # Tags
        if "tags" in self.current_record and self.current_record["tags"]:
            tags_x = panel_rect.x + 30
            tags_y = panel_rect.y + 110
            
            tags_label = self.font_small.render("Tags: ", True, self.colors['text'])
            self.screen.blit(tags_label, (tags_x, tags_y))
            tags_x += tags_label.get_width() + 10
            
            for tag in self.current_record["tags"]:
                tag_surf = self.font_small.render(tag, True, (220, 220, 255))
                tag_rect = tag_surf.get_rect(topleft=(tags_x, tags_y))
                tag_bg = tag_rect.inflate(20, 10)
                pygame.draw.rect(self.screen, self.colors['tag'], tag_bg, border_radius=10)
                self.screen.blit(tag_surf, tag_rect)
                tags_x += tag_bg.width + 10
                
                if tags_x > panel_rect.right - 50:
                    break
        
        # Content with word wrapping
        content_start_y = panel_rect.y + 150
        content_width = panel_rect.width - 60
        
        wrapped_text = textwrap.wrap(self.current_record["content"], width=80)
        for i, line in enumerate(wrapped_text):
            line_surface = self.font.render(line, True, self.colors['text'])
            line_y = content_start_y + i * 30
            
            # Stop rendering if we're out of the panel
            if line_y > panel_rect.bottom - 40:
                more_text = self.font.render("...", True, self.colors['text'])
                self.screen.blit(more_text, (panel_rect.x + 30, line_y))
                break
                
            self.screen.blit(line_surface, (panel_rect.x + 30, line_y))
    
    def draw_search_interface(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Create panel
        panel_rect = pygame.Rect(self.width // 2 - 400, 50, 800, self.height - 100)
        pygame.draw.rect(self.screen, self.colors['panel'], panel_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], panel_rect, 3)
        
        # Title
        title = self.font_large.render("Search Cosmic Knowledge", True, self.colors['accent1'])
        title_rect = title.get_rect(center=(panel_rect.centerx, panel_rect.y + 40))
        self.screen.blit(title, title_rect)
        
        # Search box
        search_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 100, panel_rect.width - 100, 50)
        pygame.draw.rect(self.screen, (40, 40, 60), search_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], search_rect, 2)
        
        search_text = self.font.render(self.search_text, True, self.colors['text'])
        self.screen.blit(search_text, (search_rect.x + 20, search_rect.y + 15))
        
        # Blinking cursor if active
        if self.search_active and time.time() % 1 > 0.5:
            cursor_x = search_rect.x + 20 + search_text.get_width()
            pygame.draw.line(
                self.screen, self.colors['text'],
                (cursor_x, search_rect.y + 15),
                (cursor_x, search_rect.y + 35),
                2
            )
        
        # Search button
        search_button = pygame.Rect(panel_rect.x + 250, panel_rect.y + 170, 300, 50)
        pygame.draw.rect(self.screen, (40, 60, 100), search_button)
        pygame.draw.rect(self.screen, self.colors['accent2'], search_button, 2)
        
        button_text = self.font.render("Search Records", True, self.colors['text'])
        button_rect = button_text.get_rect(center=search_button.center)
        self.screen.blit(button_text, button_rect)
        
        # Close button
        close_rect = pygame.Rect(panel_rect.right - 60, panel_rect.top + 20, 40, 40)
        pygame.draw.rect(self.screen, (100, 30, 30), close_rect)
        
        close_text = self.font_medium.render("×", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=close_rect.center)
        self.screen.blit(close_text, close_text_rect)
        
        # Results
        if self.is_searching:
            # Draw results title
            if self.search_results:
                results_title = self.font_medium.render(
                    f"Found {len(self.search_results)} Records", 
                    True, self.colors['accent2']
                )
            else:
                results_title = self.font_medium.render(
                    "No Records Found", 
                    True, self.colors['warning']
                )
                
            results_title_rect = results_title.get_rect(
                centerx=panel_rect.centerx, 
                top=panel_rect.y + 240
            )
            self.screen.blit(results_title, results_title_rect)
            
            # Draw results
            start_y = panel_rect.y + 280
            result_height = 100
            
            for i, result in enumerate(self.search_results[:5]):  # Show top 5 results
                result_rect = pygame.Rect(
                    panel_rect.x + 50, 
                    start_y + i * result_height, 
                    panel_rect.width - 100, 
                    result_height - 10
                )
                pygame.draw.rect(self.screen, (30, 30, 50), result_rect)
                pygame.draw.rect(self.screen, self.colors['highlight'], result_rect, 1)
                
                # Title
                title = self.font.render(result["title"], True, self.colors['accent1'])
                self.screen.blit(title, (result_rect.x + 20, result_rect.y + 10))
                
                # Category
                category = self.font_small.render(
                    f"Category: {result.get('category', 'Unknown')}", 
                    True, self.colors['accent2']
                )
                self.screen.blit(category, (result_rect.x + 20, result_rect.y + 40))
                
                # Preview
                preview = result["content"][:70] + "..." if len(result["content"]) > 70 else result["content"]
                preview_text = self.font_small.render(preview, True, self.colors['text'])
                self.screen.blit(preview_text, (result_rect.x + 20, result_rect.y + 65))
                
            # Show more results text if applicable
            if len(self.search_results) > 5:
                more_text = self.font_small.render(
                    f"{len(self.search_results) - 5} more results found. Refine your search to see more specific records.", 
                    True, self.colors['text']
                )
                more_rect = more_text.get_rect(
                    centerx=panel_rect.centerx,
                    top=start_y + 5 * result_height
                )
                self.screen.blit(more_text, more_rect)
    
    def draw_input_interface(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 220))
        self.screen.blit(overlay, (0, 0))
        
        # Create panel
        panel_rect = pygame.Rect(self.width // 2 - 400, 50, 800, self.height - 100)
        pygame.draw.rect(self.screen, self.colors['panel'], panel_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], panel_rect, 3)
        
        # Title
        title = self.font_large.render("Add Cosmic Knowledge", True, self.colors['accent1'])
        title_rect = title.get_rect(center=(panel_rect.centerx, panel_rect.y + 40))
        self.screen.blit(title, title_rect)
        
        # Category selection
        category_label = self.font.render("Category:", True, self.colors['text'])
        self.screen.blit(category_label, (panel_rect.x + 50, panel_rect.y + 100))
        
        # Draw selected category
        category_text = self.font.render(self.selected_category or "Select Category", True, self.colors['accent2'])
        self.screen.blit(category_text, (panel_rect.x + 180, panel_rect.y + 100))
        
        # Title input
        title_label = self.font.render("Title:", True, self.colors['text'])
        self.screen.blit(title_label, (panel_rect.x + 50, panel_rect.y + 150))
        
        title_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 180, panel_rect.width - 100, 50)
        pygame.draw.rect(self.screen, (40, 40, 60), title_rect)
        border_color = self.colors['accent1'] if self.input_mode == "title" else self.colors['highlight']
        pygame.draw.rect(self.screen, border_color, title_rect, 2)
        
        title_text = self.font.render(self.input_title, True, self.colors['text'])
        self.screen.blit(title_text, (title_rect.x + 20, title_rect.y + 15))
        
        # Content input
        content_label = self.font.render("Cosmic Information:", True, self.colors['text'])
        self.screen.blit(content_label, (panel_rect.x + 50, panel_rect.y + 250))
        
        content_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 280, panel_rect.width - 100, 200)
        pygame.draw.rect(self.screen, (40, 40, 60), content_rect)
        border_color = self.colors['accent1'] if self.input_mode == "content" else self.colors['highlight']
        pygame.draw.rect(self.screen, border_color, content_rect, 2)
        
        # Render multiline content
        lines = self.input_content.split('\n')
        for i, line in enumerate(lines):
            if i * 25 < content_rect.height - 30:  # Check if we're still in the content box
                line_surf = self.font.render(line, True, self.colors['text'])
                self.screen.blit(line_surf, (content_rect.x + 20, content_rect.y + 15 + i * 25))
        
        # Tags input
        tags_label = self.font.render("Tags (comma separated):", True, self.colors['text'])
        self.screen.blit(tags_label, (panel_rect.x + 50, panel_rect.y + 500))
        
        tags_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 530, panel_rect.width - 100, 50)
        pygame.draw.rect(self.screen, (40, 40, 60), tags_rect)
        border_color = self.colors['accent1'] if self.input_mode == "tags" else self.colors['highlight']
        pygame.draw.rect(self.screen, border_color, tags_rect, 2)
        
        tags_text = self.font.render(self.input_tags, True, self.colors['text'])
        self.screen.blit(tags_text, (tags_rect.x + 20, tags_rect.y + 15))
        
        # Buttons
        save_rect = pygame.Rect(panel_rect.x + 150, panel_rect.y + panel_rect.height - 80, 200, 50)
        pygame.draw.rect(self.screen, (30, 100, 50), save_rect)
        pygame.draw.rect(self.screen, (100, 200, 120), save_rect, 2)
        
        save_text = self.font.render("Save Record", True, (220, 255, 220))
        save_text_rect = save_text.get_rect(center=save_rect.center)
        self.screen.blit(save_text, save_text_rect)
        
        cancel_rect = pygame.Rect(panel_rect.x + 450, panel_rect.y + panel_rect.height - 80, 200, 50)
        pygame.draw.rect(self.screen, (100, 30, 50), cancel_rect)
        pygame.draw.rect(self.screen, (200, 100, 120), cancel_rect, 2)
        
        cancel_text = self.font.render("Cancel", True, (255, 220, 220))
        cancel_text_rect = cancel_text.get_rect(center=cancel_rect.center)
        self.screen.blit(cancel_text, cancel_text_rect)
        
        # Blinking cursor for active input
        if self.input_mode and time.time() % 1 > 0.5:
            cursor_pos = None
            if self.input_mode == "title":
                text_width = title_text.get_width()
                cursor_pos = (title_rect.x + 20 + text_width, title_rect.y + 15)
                cursor_height = 30
            elif self.input_mode == "content":
                # Find position in the current line
                current_line_index = len(lines) - 1
                if current_line_index >= 0:
                    current_line = lines[current_line_index]
                    line_surf = self.font.render(current_line, True, self.colors['text'])
                    text_width = line_surf.get_width()
                    cursor_pos = (
                        content_rect.x + 20 + text_width, 
                        content_rect.y + 15 + current_line_index * 25
                    )
                    cursor_height = 25
            elif self.input_mode == "tags":
                text_width = tags_text.get_width()
                cursor_pos = (tags_rect.x + 20 + text_width, tags_rect.y + 15)
                cursor_height = 30
                
            if cursor_pos:
                pygame.draw.line(
                    self.screen, self.colors['text'],
                    cursor_pos,
                    (cursor_pos[0], cursor_pos[1] + cursor_height),
                    2
                )
    
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
                except Exception as e:
                    print(f"Error loading record {filename}: {e}")
                    continue
                    
        # Sort by date (newest first)
        self.records.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    def search_records(self):
        if not self.search_text.strip():
            self.show_notification("Please enter a search term", color=self.colors['warning'])
            return
            
        query = self.search_text.lower()
        self.search_results = []
        
        # Search in all categories
        for category in self.categories:
            category_folder = os.path.join(self.library_path, category.replace(" ", "_"))
            if not os.path.exists(category_folder):
                continue
                
            for filename in os.listdir(category_folder):
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join(category_folder, filename), 'r', encoding='utf-8') as f:
                            record = json.load(f)
                            
                            # Add category to record for display
                            record['category'] = category
                            
                            # Search in title, content and tags
                            if query in record.get('title', '').lower() or \
                               query in record.get('content', '').lower() or \
                               any(query in tag.lower() for tag in record.get('tags', [])):
                                self.search_results.append(record)
                    except:
                        continue
        
        # Sort results by relevance (title matches first, then tags, then content)
        def relevance_score(record):
            title_match = query in record.get('title', '').lower()
            tag_match = any(query in tag.lower() for tag in record.get('tags', []))
            content_match = query in record.get('content', '').lower()
            
            if title_match:
                return 0  # Highest priority
            elif tag_match:
                return 1
            elif content_match:
                return 2
            return 3
        
        self.search_results.sort(key=relevance_score)
        self.is_searching = True
        
        # Show notification
        if self.search_results:
            self.show_notification(f"Found {len(self.search_results)} cosmic records", color=self.colors['success'])
        else:
            self.show_notification("No cosmic records found for your query", color=self.colors['warning'])
    
    def save_record(self):
        if not self.selected_category:
            self.show_notification("Please select a category", color=self.colors['warning'])
            return
            
        if not self.input_title.strip():
            self.show_notification("Please provide a title", color=self.colors['warning'])
            return
            
        if not self.input_content.strip():
            self.show_notification("Please provide cosmic information", color=self.colors['warning'])
            return
            
        # Process tags
        tags = [tag.strip() for tag in self.input_tags.split(',') if tag.strip()]
        
        record = {
            "title": self.input_title,
            "content": self.input_content,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": self.username,
            "tags": tags
        }
        
        # Save to file
        category_folder = os.path.join(self.library_path, self.selected_category.replace(" ", "_"))
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)
            
        filename = os.path.join(category_folder, f"{int(time.time())}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
            
        # Update counts
        self.total_records += 1
        
        # Show notification and reset form
        self.show_notification("Cosmic knowledge recorded successfully", color=self.colors['success'])
        self.input_active = False
        
        # If we're in a category view, refresh it
        if self.active_category == self.selected_category:
            self.load_records()
    
    def handle_click(self, pos):
        if self.viewing_record_detail:
            # Handle detail view clicks
            panel_rect = pygame.Rect(self.width // 2 - 450, 50, 900, self.height - 100)
            
            # Close button
            close_rect = pygame.Rect(panel_rect.right - 60, panel_rect.top + 20, 40, 40)
            if close_rect.collidepoint(pos):
                self.viewing_record_detail = False
                return
                
            return
            
        if self.search_active:
            # Handle search interface clicks
            panel_rect = pygame.Rect(self.width // 2 - 400, 50, 800, self.height - 100)
            
            # Close button
            close_rect = pygame.Rect(panel_rect.right - 60, panel_rect.top + 20, 40, 40)
            if close_rect.collidepoint(pos):
                self.search_active = False
                self.is_searching = False
                return
                
            # Search box
            search_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 100, panel_rect.width - 100, 50)
            if search_rect.collidepoint(pos):
                self.search_active = True
                return
                
            # Search button
            search_button = pygame.Rect(panel_rect.x + 250, panel_rect.y + 170, 300, 50)
            if search_button.collidepoint(pos):
                self.search_records()
                return
                
            # Result clicks
            if self.is_searching and self.search_results:
                start_y = panel_rect.y + 280
                result_height = 100
                
                for i, result in enumerate(self.search_results[:5]):
                    result_rect = pygame.Rect(
                        panel_rect.x + 50, 
                        start_y + i * result_height, 
                        panel_rect.width - 100, 
                        result_height - 10
                    )
                    
                    if result_rect.collidepoint(pos):
                        # View this record
                        self.current_record = result
                        self.active_category = result.get('category')
                        self.viewing_record_detail = True
                        self.search_active = False
                        return
                        
            return
            
        if self.input_active:
            # Handle input dialog clicks
            panel_rect = pygame.Rect(self.width // 2 - 400, 50, 800, self.height - 100)