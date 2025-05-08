import pygame
import pygame.gfxdraw
import os
import json
import random
import math
import time
from datetime import datetime
import textwrap

class CosmicArchivesExplorer:
    def __init__(self, username="behicof", timestamp="2025-04-17 14:27:41"):
        pygame.init()
        self.archives_path = "cosmic_grand_archives"
        self.width, self.height = 1280, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cosmic Archives Explorer: Five Centuries of Knowledge")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # User info
        self.username = username
        self.timestamp = timestamp
        
        # Load fonts
        self.font_tiny = pygame.font.SysFont('Arial', 12)
        self.font_small = pygame.font.SysFont('Arial', 16)
        self.font = pygame.font.SysFont('Arial', 24)
        self.font_medium = pygame.font.SysFont('Arial', 28)
        self.font_large = pygame.font.SysFont('Arial', 36)
        self.font_huge = pygame.font.SysFont('Arial', 48)
        
        # Colors
        self.colors = {
            'background': (5, 10, 30),
            'text': (220, 220, 255),
            'highlight': (100, 100, 200),
            'accent1': (180, 120, 255),
            'accent2': (100, 200, 220),
            'accent3': (220, 150, 100),
            'button': (40, 40, 80),
            'button_highlight': (60, 60, 120),
            'panel': (20, 20, 40, 220),
            'success': (100, 200, 100),
            'warning': (200, 150, 50),
            'tag': (60, 80, 120)
        }
        
        # Background elements
        self.stars = []
        self.energy_particles = []
        self.create_stars(300)
        self.create_energy_particles(70)
        
        # Archive data
        self.archive_info = self.load_archive_info()
        self.time_periods = self.archive_info.get("time_periods", [])
        self.domains = self.archive_info.get("domains", [])
        self.selected_period = None
        self.selected_domain = None
        self.selected_record = None
        self.record_page = 0
        
        # UI state
        self.view_mode = "main"  # "main", "period", "domain", "record", "search"
        self.records = []
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Search
        self.search_active = False
        self.search_text = ""
        self.search_results = []
        self.search_category = "all"  # "all", "title", "content", "wisdom", "tags"
        
        # Navigation history
        self.nav_history = []
        
        # Notification system
        self.notification = None
        self.notification_timer = 0
        
        # Animation timers
        self.animation_time = 0
    
    def load_archive_info(self):
        """Load archive metadata from the master index"""
        try:
            index_path = os.path.join(self.archives_path, "master_index.json")
            if os.path.exists(index_path):
                with open(index_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    "archive_name": "Cosmic Archives",
                    "total_records": 0,
                    "time_periods": [],
                    "domains": []
                }
        except Exception as e:
            print(f"Error loading archive info: {e}")
            return {
                "archive_name": "Cosmic Archives",
                "total_records": 0,
                "time_periods": [],
                "domains": []
            }
    
    def load_period_info(self, period):
        """Load period-specific information"""
        try:
            period_dir = f"{period['start_year']}-{period['end_year']}_{period['name'].replace(' ', '_')}"
            index_path = os.path.join(self.archives_path, period_dir, "period_index.json")
            
            if os.path.exists(index_path):
                with open(index_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    "period_name": period["name"],
                    "total_records": 0,
                    "records_by_domain": {}
                }
        except Exception as e:
            print(f"Error loading period info: {e}")
            return {
                "period_name": period["name"],
                "total_records": 0,
                "records_by_domain": {}
            }
    
    def load_domain_records(self, period, domain):
        """Load all records for a specific domain within a period"""
        records = []
        try:
            period_dir = f"{period['start_year']}-{period['end_year']}_{period['name'].replace(' ', '_')}"
            domain_dir = domain.replace(' ', '_')
            domain_path = os.path.join(self.archives_path, period_dir, domain_dir)
            
            if os.path.exists(domain_path):
                for filename in os.listdir(domain_path):
                    if filename.endswith('.json'):
                        try:
                            with open(os.path.join(domain_path, filename), 'r', encoding='utf-8') as f:
                                record = json.load(f)
                                records.append(record)
                        except Exception as e:
                            print(f"Error loading record {filename}: {e}")
            
            # Sort by date
            records.sort(key=lambda x: x.get("date_recorded", ""), reverse=True)
        except Exception as e:
            print(f"Error loading domain records: {e}")
        
        return records
    
    def load_record(self, record_id):
        """Load a specific record by ID"""
        # Parse the ID to find the domain and period
        if not record_id:
            return None
            
        parts = record_id.split('-')
        if len(parts) < 3:
            return None
            
        domain_prefix = parts[0]
        period_year = parts[1]
        
        # Find matching domain
        domain = None
        for d in self.domains:
            if d.replace(' ', '').startswith(domain_prefix):
                domain = d
                break
        
        if not domain:
            return None
        
        # Find matching period
        period = None
        for p in self.time_periods:
            if str(p["start_year"]) == period_year:
                period = p
                break
        
        if not period:
            return None
        
        # Load all records from domain and find the one with matching ID
        records = self.load_domain_records(period, domain)
        for record in records:
            if record.get("id") == record_id:
                return record
                
        return None
    
    def create_stars(self, count):
        """Create background stars"""
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
        """Create energy particles that float around"""
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
        """Update star twinkle effect"""
        for star in self.stars:
            # Make stars twinkle
            brightness = 150 + 105 * math.sin(time.time() * star['twinkle_rate'] * 10)
            star['color'] = (brightness, brightness, brightness)
    
    def update_energy_particles(self):
        """Update energy particle movement"""
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
        """Draw the cosmic background gradient"""
        for y in range(0, self.height, 2):
            gradient_factor = y / self.height
            r = int(5 + 10 * gradient_factor)
            g = int(8 + 2 * gradient_factor)
            b = int(25 + 5 * gradient_factor)
            
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y), 2)
    
    def draw_stars(self):
        """Draw background stars"""
        for star in self.stars:
            x, y = star['pos']
            size = star['size']
            color = star['color']
            pygame.gfxdraw.filled_circle(self.screen, int(x), int(y), int(size), color)
    
    def draw_energy_particles(self):
        """Draw floating energy particles"""
        for particle in self.energy_particles:
            x, y = particle['pos']
            size = particle['size']
            base_color = particle['color']
            alpha = int(255 * particle['life'])
            color = (*base_color[:3], alpha)
            
            for i in range(3):
                glow_size = size * (3 - i) / 2
                glow_alpha = alpha // (i + 1)
                glow_color = (*base_color[:3], glow_alpha)
                pygame.gfxdraw.filled_circle(
                    self.screen, int(x), int(y), int(glow_size), glow_color
                )
    
    def draw_main_interface(self):
        """Draw the main archives interface"""
        # Draw title
        title = self.font_huge.render("Cosmic Archives Explorer", True, self.colors['accent1'])
        title_rect = title.get_rect(center=(self.width // 2, 70))
        self.screen.blit(title, title_rect)
        
        # Draw subtitle
        subtitle = self.font_medium.render("Five Centuries of Galactic Knowledge", True, self.colors['accent2'])
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 120))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw user info
        user_text = self.font_small.render(
            f"Archivist: {self.username} | Access Date: {self.timestamp}", 
            True, (180, 180, 220)
        )
        self.screen.blit(user_text, (20, 20))
        
        # Draw archive stats
        stats_text = self.font_small.render(
            f"Total Archives: {self.archive_info.get('total_records', 0)} records across {len(self.time_periods)} time periods", 
            True, (180, 180, 220)
        )
        stats_rect = stats_text.get_rect(right=self.width - 20, top=20)
        self.screen.blit(stats_text, stats_rect)
        
        # Draw search button
        search_rect = pygame.Rect(self.width - 180, 60, 160, 40)
        pygame.draw.rect(self.screen, self.colors['button'], search_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], search_rect, 2)
        
        search_text = self.font.render("Search", True, self.colors['text'])
        search_text_rect = search_text.get_rect(center=search_rect.center)
        self.screen.blit(search_text, search_text_rect)
        
        # Draw time periods in a timeline
        timeline_y = 170
        period_width = self.width // len(self.time_periods) if self.time_periods else self.width
        
        # Draw timeline bar
        timeline_rect = pygame.Rect(50, timeline_y, self.width - 100, 8)
        pygame.draw.rect(self.screen, self.colors['accent2'], timeline_rect)
        
        # Draw period markers and labels
        for i, period in enumerate(self.time_periods):
            # Calculate position
            x_pos = 50 + (i + 0.5) * (self.width - 100) / len(self.time_periods)
            
            # Draw period marker
            marker_radius = 12
            pygame.draw.circle(self.screen, self.colors['accent1'], (int(x_pos), timeline_y + 4), marker_radius)
            pygame.draw.circle(self.screen, self.colors['text'], (int(x_pos), timeline_y + 4), marker_radius - 2)
            
            # Draw year label
            year_text = self.font_small.render(f"{period['start_year']}-{period['end_year']}", True, self.colors['text'])
            year_rect = year_text.get_rect(center=(x_pos, timeline_y + 30))
            self.screen.blit(year_text, year_rect)
            
            # Draw period name
            name_text = self.font.render(period['name'], True, self.colors['accent1'])
            name_rect = name_text.get_rect(center=(x_pos, timeline_y + 60))
            self.screen.blit(name_text, name_rect)
            
            # Draw selection box with animation
            pulse = 0.5 + 0.5 * math.sin(time.time() * 2 + i * 0.5)
            glow_size = int(2 + 2 * pulse)
            
            select_rect = pygame.Rect(x_pos - period_width//2 + 20, timeline_y + 90, period_width - 40, 60)
            pygame.draw.rect(self.screen, self.colors['button'], select_rect)
            pygame.draw.rect(self.screen, self.colors['highlight'], select_rect, glow_size)
            
            select_text = self.font.render("Explore", True, self.colors['text'])
            select_text_rect = select_text.get_rect(center=select_rect.center)
            self.screen.blit(select_text, select_text_rect)
        
        # Draw domain quick access section
        domain_title = self.font_medium.render("Knowledge Domains", True, self.colors['accent3'])
        domain_title_rect = domain_title.get_rect(center=(self.width // 2, 280))
        self.screen.blit(domain_title, domain_title_rect)
        
        # Draw domains in a grid
        domains_per_row = 4
        domain_width = self.width // domains_per_row - 20
        domain_height = 80
        
        for i, domain in enumerate(self.domains[:12]):  # Show only first 12 domains on main page
            row = i // domains_per_row
            col = i % domains_per_row
            
            x = col * (domain_width + 20) + 10
            y = 330 + row * (domain_height + 10)
            
            # Draw domain button
            domain_rect = pygame.Rect(x, y, domain_width, domain_height)
            
            # Animated glow
            pulse = 0.5 + 0.5 * math.sin(time.time() * 1.5 + i * 0.3)
            domain_color = (
                int(40 + 20 * pulse),
                int(40 + 10 * pulse),
                int(80 + 20 * pulse)
            )
            
            pygame.draw.rect(self.screen, domain_color, domain_rect)
            pygame.draw.rect(self.screen, self.colors['highlight'], domain_rect, 2)
            
            # Draw domain name
            lines = textwrap.wrap(domain, width=15)
            line_height = self.font.get_height()
            total_height = line_height * len(lines)
            start_y = domain_rect.centery - total_height // 2
            
            for j, line in enumerate(lines):
                line_surf = self.font.render(line, True, self.colors['text'])
                line_rect = line_surf.get_rect(center=(domain_rect.centerx, start_y + j * line_height))
                self.screen.blit(line_surf, line_rect)
        
        # If there are more domains, add a "More" button
        if len(self.domains) > 12:
            more_rect = pygame.Rect(self.width // 2 - 80, 690, 160, 50)
            pygame.draw.rect(self.screen, self.colors['button'], more_rect)
            pygame.draw.rect(self.screen, self.colors['highlight'], more_rect, 2)
            
            more_text = self.font.render("More Domains", True, self.colors['text'])
            more_text_rect = more_text.get_rect(center=more_rect.center)
            self.screen.blit(more_text, more_text_rect)
    
    def draw_period_interface(self):
        """Draw the period browse interface"""
        if not self.selected_period:
            self.view_mode = "main"
            return
            
        # Load period info if not loaded
        period_info = self.load_period_info(self.selected_period)
        
        # Draw back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['button'], back_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], back_rect, 2)
        
        back_text = self.font_small.render("Back", True, self.colors['text'])
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Draw period title
        title = self.font_large.render(
            f"{self.selected_period['name']} ({self.selected_period['start_year']}-{self.selected_period['end_year']})", 
            True, self.colors['accent1']
        )
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw period stats
        stats_text = self.font.render(
            f"Records: {period_info.get('total_records', 0)}", 
            True, self.colors['accent2']
        )
        stats_rect = stats_text.get_rect(center=(self.width // 2, 100))
        self.screen.blit(stats_text, stats_rect)
        
        # Draw domains grid
        domains_per_row = 3
        domain_width = self.width // domains_per_row - 40
        domain_height = 120
        
        # Sort domains by record count (most records first)
        domain_counts = period_info.get("records_by_domain", {})
        sorted_domains = sorted(
            self.domains, 
            key=lambda d: domain_counts.get(d, 0), 
            reverse=True
        )
        
        for i, domain in enumerate(sorted_domains):
            row = i // domains_per_row
            col = i % domains_per_row
            
            x = col * (domain_width + 40) + 30
            y = 150 + row * (domain_height + 30)
            
            # Skip domains that would render below the visible area
            if y > self.height - 30:
                continue
                
            # Draw domain panel
            domain_rect = pygame.Rect(x, y, domain_width, domain_height)
            
            # Color based on record count
            record_count = domain_counts.get(domain, 0)
            if record_count > 0:
                # Use a gradient from cool to warm based on record count
                max_count = max(domain_counts.values()) if domain_counts else 1
                intensity = min(1.0, record_count / (max_count * 0.7))  # Cap at 70% to avoid too bright colors
                color = (
                    int(40 + 100 * intensity),
                    int(40 + 20 * (1 - intensity)),
                    int(80 + 20 * (1 - intensity))
                )
            else:
                color = (30, 30, 50)  # Muted color for domains with no records
            
            # Draw with animated pulse if has records
            if record_count > 0:
                pulse = 0.5 + 0.5 * math.sin(time.time() * 1.5 + i * 0.3)
                glow_size = int(2 + 3 * pulse)
                
                # Adjust color with pulse
                pulse_color = (
                    min(255, color[0] + int(20 * pulse)),
                    min(255, color[1] + int(10 * pulse)),
                    min(255, color[2] + int(30 * pulse))
                )
                
                pygame.draw.rect(self.screen, pulse_color, domain_rect)
                pygame.draw.rect(self.screen, self.colors['highlight'], domain_rect, glow_size)
            else:
                pygame.draw.rect(self.screen, color, domain_rect)
                pygame.draw.rect(self.screen, self.colors['highlight'], domain_rect, 1)
            
            # Draw domain name
            domain_text = self.font.render(domain, True, self.colors['text'])
            domain_text_rect = domain_text.get_rect(centerx=domain_rect.centerx, top=domain_rect.top + 15)
            self.screen.blit(domain_text, domain_text_rect)
            
            # Draw record count
            count_text = self.font.render(f"{record_count} Records", True, self.colors['accent2'])
            count_text_rect = count_text.get_rect(centerx=domain_rect.centerx, top=domain_rect.top + 50)
            self.screen.blit(count_text, count_text_rect)
            
            # Draw explore button if has records
            if record_count > 0:
                explore_rect = pygame.Rect(domain_rect.centerx - 60, domain_rect.bottom - 35, 120, 30)
                pygame.draw.rect(self.screen, self.colors['button'], explore_rect)
                pygame.draw.rect(self.screen, self.colors['accent3'], explore_rect, 2)
                
                explore_text = self.font_small.render("Explore Domain", True, self.colors['text'])
                explore_text_rect = explore_text.get_rect(center=explore_rect.center)
                self.screen.blit(explore_text, explore_text_rect)
    
    def draw_domain_interface(self):
        """Draw the domain browse interface with records list"""
        if not self.selected_period or not self.selected_domain:
            self.view_mode = "period"
            return
            
        # Draw back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['button'], back_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], back_rect, 2)
        
        back_text = self.font_small.render("Back", True, self.colors['text'])
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Draw domain title
        title = self.font_large.render(self.selected_domain, True, self.colors['accent1'])
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw period
        period_text = self.font.render(
            f"{self.selected_period['name']} ({self.selected_period['start_year']}-{self.selected_period['end_year']})", 
            True, self.colors['accent2']
        )
        period_rect = period_text.get_rect(center=(self.width // 2, 100))
        self.screen.blit(period_text, period_rect)
        
        # Load records if not loaded
        if not self.records:
            self.records = self.load_domain_records(self.selected_period, self.selected_domain)
            
        # Draw records count
        count_text = self.font.render(f"{len(self.records)} Records", True, self.colors['accent3'])
        count_rect = count_text.get_rect(right=self.width - 20, top=20)
        self.screen.blit(count_text, count_rect)
        
        # Draw records list
        if not self.records:
            # No records message
            no_records = self.font.render("No records found in this domain for this time period.", True, self.colors['text'])
            no_records_rect = no_records.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(no_records, no_records_rect)
        else:
            # Draw scrollable record list
            record_height = 140
            start_y = 150 - self.scroll_offset
            
            for i, record in enumerate(self.records):
                y_pos = start_y + i * record_height
                
                # Skip records that are off-screen
                if y_pos + record_height < 0 or y_pos > self.height:
                    continue
                
                # Draw record panel
                record_rect = pygame.Rect(self.width // 2 - 400, y_pos, 800, record_height - 20)
                
                # Highlight effect based on verification level
                verification = record.get("verification_level", 0)
                highlight_color = (
                    40 + verification * 10,
                    40 + verification * 5,
                    80 + verification * 5
                )
                
                pygame.draw.rect(self.screen, highlight_color, record_rect)
                pygame.draw.rect(self.screen, self.colors['highlight'], record_rect, 2)
                
                # Title
                title = self.font_medium.render(record.get("title", "Untitled Record"), True, self.colors['accent1'])
                title_rect = title.get_rect(topleft=(record_rect.x + 20, record_rect.y + 15))
                self.screen.blit(title, title_rect)
                
                # Date and source
                date_source = self.font_small.render(
                    f"Recorded: {record.get('date_recorded', 'Unknown')} | Source: {record.get('source_civilization', 'Unknown')}", 
                    True, self.colors['accent2']
                )
                date_source_rect = date_source.get_rect(topleft=(record_rect.x + 20, record_rect.y + 50))
                self.screen.blit(date_source, date_source_rect)
                
                # Format
                format_text = self.font_small.render(
                    f"Format: {record.get('format', 'Unknown')}", 
                    True, self.colors['accent3']
                )
                format_rect = format_text.get_rect(topleft=(record_rect.x + 20, record_rect.y + 75))
                self.screen.blit(format_text, format_rect)
                
                # Preview of wisdom
                preview = record.get("wisdom", "")[:100] + "..." if len(record.get("wisdom", "")) > 100 else record.get("wisdom", "")
                if preview:
                    preview_text = self.font_small.render(preview, True, self.colors['text'])
                    preview_rect = preview_text.get_rect(topleft=(record_rect.x + 20, record_rect.y + 100))
                    self.screen.blit(preview_text, preview_rect)
                
                # Tags
                if "tags" in record and record["tags"]:
                    tags_x = record_rect.right - 300
                    tags_y = record_rect.y + 15
                    
                    for tag in record["tags"][:3]:  # Show up to 3 tags
                        tag_surf = self.font_tiny.render(tag, True, (220, 220, 255))
                        tag_rect = tag_surf.get_rect(topleft=(tags_x, tags_y))
                        tag_bg = tag_rect.inflate(10, 5)
                        
                        pygame.draw.rect(self.screen, self.colors['tag'], tag_bg, border_radius=5)
                        self.screen.blit(tag_surf, tag_rect)
                        
                        tags_x += tag_bg.width + 10
                        
                        if tags_x > record_rect.right - 10:
                            break
            
            # Calculate max scroll
            total_height = len(self.records) * record_height
            self.max_scroll = max(0, total_height - (self.height - 150))
            
            # Draw scrollbar if needed
            if self.max_scroll > 0:
                scrollbar_height = max(50, (self.height - 150) * (self.height - 150) / total_height)
                scrollbar_pos = 150 + (self.height - 150 - scrollbar_height) * (self.scroll_offset / self.max_scroll)
                
                scrollbar_rect = pygame.Rect(self.width - 20, scrollbar_pos, 10, scrollbar_height)
                pygame.draw.rect(self.screen, self.colors['highlight'], scrollbar_rect)
    
    def draw_record_interface(self):
        """Draw detailed view of a single record"""
        if not self.selected_record:
            self.view_mode = "domain"
            return
            
        # Draw back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['button'], back_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], back_rect, 2)
        
        back_text = self.font_small.render("Back", True, self.colors['text'])
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Record panel
        panel_rect = pygame.Rect(50, 80, self.width - 100, self.height - 100)
        pygame.draw.rect(self.screen, (20, 20, 40, 240), panel_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], panel_rect, 3)
        
        # Title
        title_text = self.font_large.render(self.selected_record.get("title", "Untitled Record"), True, self.colors['accent1'])
        title_rect = title_text.get_rect(centerx=panel_rect.centerx, top=panel_rect.top + 20)
        self.screen.blit(title_text, title_rect)
        
        # Metadata
        metadata_y = title_rect.bottom + 20
        
        # Source and date
        source_date = self.font.render(
            f"Source: {self.selected_record.get('source_civilization', 'Unknown')} | Date: {self.selected_record.get('date_recorded', 'Unknown')}", 
            True, self.colors['accent2']
        )
        source_date_rect = source_date.get_rect(centerx=panel_rect.centerx, top=metadata_y)
        self.screen.blit(source_date, source_date_rect)
        
        # Format and verification
        format_verify = self.font.render(
            f"Format: {self.selected_record.get('format', 'Unknown')} | Verification Level: {self.selected_record.get('verification_level', 0)}/5", 
            True, self.colors['accent3']
        )
        format_verify_rect = format_verify.get_rect(centerx=panel_rect.centerx, top=metadata_y + 30)
        self.screen.blit(format_verify, format_verify_rect)
        
        # Frequency signature if available
        if "frequency_signature" in self.selected_record:
            frequency = self.font.render(
                f"Frequency Signature: {self.selected_record.get('frequency_signature')} Hz", 
                True, self.colors['accent2']
            )
            frequency_rect = frequency.get_rect(centerx=panel_rect.centerx, top=metadata_y + 60)
            self.screen.blit(frequency, frequency_rect)
            content_start_y = frequency_rect.bottom + 30
        else:
            content_start_y = format_verify_rect.bottom + 30
        
        # Tags
        if "tags" in self.selected_record and self.selected_record["tags"]:
            tags_y = content_start_y
            tags_x = panel_rect.x + 100
            
            tags_label = self.font.render("Tags:", True, self.colors['text'])
            self.screen.blit(tags_label, (panel_rect.x + 30, tags_y))
            
            for tag in self.selected_record["tags"]:
                tag_surf = self.font_small.render(tag, True, (220, 220, 255))
                tag_rect = tag_surf.get_rect(topleft=(tags_x, tags_y + 5))
                tag_bg = tag_rect.inflate(10, 5)
                
                pygame.draw.rect(self.screen, self.colors['tag'], tag_bg, border_radius=5)
                self.screen.blit(tag_surf, tag_rect)
                
                tags_x += tag_bg.width + 10
                
                if tags_x > panel_rect.right - 100:
                    # Move to next line
                    tags_y += 30
                    tags_x = panel_rect.x + 100
            
            content_start_y = tags_y + 40
        
        # Wisdom quote
        if "wisdom" in self.selected_record and self.selected_record["wisdom"]:
            wisdom_rect = pygame.Rect(panel_rect.x + 50, content_start_y, panel_rect.width - 100, 60)
            pygame.draw.rect(self.screen, (40, 30, 60), wisdom_rect)
            pygame.draw.rect(self.screen, self.colors['accent3'], wisdom_rect, 2)
            
            # Wrap wisdom text
            wrapped_wisdom = textwrap.wrap(self.selected_record["wisdom"], width=90)
            for i, line in enumerate(wrapped_wisdom[:2]):  # Show up to 2 lines
                wisdom_text = self.font.render(line, True, self.colors['accent2'])
                wisdom_text_rect = wisdom_text.get_rect(centerx=wisdom_rect.centerx, top=wisdom_rect.top + 10 + i * 30)
                self.screen.blit(wisdom_text, wisdom_text_rect)
                
            content_start_y = wisdom_rect.bottom + 30
        
        # Main content
        content_rect = pygame.Rect(panel_rect.x + 30, content_start_y, panel_rect.width - 60, panel_rect.bottom - content_start_y - 80)
        pygame.draw.rect(self.screen, (30, 30, 50), content_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], content_rect, 1)
        
        # Wrap and render content
        if "content" in self.selected_record:
            content = self.selected_record["content"]
            wrapped_content = textwrap.wrap(content, width=80)
            
            line_height = self.font_small.get_height()
            max_lines = content_rect.height // line_height - 1
            
            # Handle scrolling for content
            start_line = self.record_page * max_lines
            end_line = min(start_line + max_lines, len(wrapped_content))
            
            for i, line in enumerate(wrapped_content[start_line:end_line]):
                line_text = self.font_small.render(line, True, self.colors['text'])
                self.screen.blit(line_text, (content_rect.x + 15, content_rect.y + 15 + i * line_height))
            
            # Draw page navigation if needed
            total_pages = (len(wrapped_content) + max_lines - 1) // max_lines
            
            if total_pages > 1:
                page_text = self.font.render(f"Page {self.record_page + 1}/{total_pages}", True, self.colors['text'])
                page_rect = page_text.get_rect(centerx=panel_rect.centerx, bottom=panel_rect.bottom - 20)
                self.screen.blit(page_text, page_rect)
                
                # Previous page button
                if self.record_page > 0:
                    prev_rect = pygame.Rect(page_rect.left - 100, page_rect.top, 80, 30)
                    pygame.draw.rect(self.screen, self.colors['button'], prev_rect)
                    pygame.draw.rect(self.screen, self.colors['highlight'], prev_rect, 2)
                    
                    prev_text = self.font_small.render("Previous", True, self.colors['text'])
                    prev_text_rect = prev_text.get_rect(center=prev_rect.center)
                    self.screen.blit(prev_text, prev_text_rect)
                
                # Next page button
                if self.record_page < total_pages - 1:
                    next_rect = pygame.Rect(page_rect.right + 20, page_rect.top, 80, 30)
                    pygame.draw.rect(self.screen, self.colors['button'], next_rect)
                    pygame.draw.rect(self.screen, self.colors['highlight'], next_rect, 2)
                    
                    next_text = self.font_small.render("Next", True, self.colors['text'])
                    next_text_rect = next_text.get_rect(center=next_rect.center)
                    self.screen.blit(next_text, next_text_rect)
        
        # Related records
        if "related_records" in self.selected_record and self.selected_record["related_records"]:
            related_label = self.font.render("Related Records:", True, self.colors['accent2'])
            related_rect = related_label.get_rect(left=panel_rect.x + 30, bottom=panel_rect.bottom - 50)
            self.screen.blit(related_label, related_rect)
            
            x_pos = related_rect.right + 20
            for i, related in enumerate(self.selected_record["related_records"][:3]):  # Show up to 3 related records
                related_text = self.font_small.render(related.get("title", ""), True, self.colors['text'])
                related_text_rect = pygame.Rect(x_pos, related_rect.top - 5, 150, 30)
                
                # Draw background
                pygame.draw.rect(self.screen, self.colors['button'], related_text_rect)
                pygame.draw.rect(self.screen, self.colors['highlight'], related_text_rect, 1)
                
                # Draw truncated title
                truncated = related.get("title", "")[:15] + "..." if len(related.get("title", "")) > 15 else related.get("title", "")
                text = self.font_small.render(truncated, True, self.colors['text'])
                text_rect = text.get_rect(center=related_text_rect.center)
                self.screen.blit(text, text_rect)
                
                x_pos += 160
    
    def draw_search_interface(self):
        """Draw search interface"""
        # Draw title
        title = self.font_large.render("Search Cosmic Archives", True, self.colors['accent1'])
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, self.colors['button'], back_rect)
        pygame.draw.rect(self.screen, self.colors['highlight'], back_rect, 2)
        
        back_text = self.font_small.render("Back", True, self.colors['text'])
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Search box
        search_rect = pygame.Rect(self.width // 2 - 300, 120, 600, 50)
        pygame.draw.rect(self.screen, (40, 40, 60), search_rect)
        
        # Highlight if active
        border_color = self.colors['accent1'] if self.search_active else self.colors['highlight']
        pygame.draw.rect(self.screen, border_color, search_rect, 2)
        
        # Draw search text
        search_text_surf = self.font.render(self.search_text, True, self.colors['text'])
        self.screen.blit(search_text_surf, (search_rect.x + 20, search_rect.y + 15))
        
        # Draw blinking cursor if active
        if self.search_active and time.time() % 1 > 0.5:
            cursor_x = search_rect.x + 20 + search_text_surf.get_width()
            pygame.draw.line(
                self.screen, self.colors['text'],
                (cursor_x, search_rect.y + 15),
                (cursor_x, search_rect.y + 40),
                2
            )
        
        # Search button
        search_button = pygame.Rect(self.width // 2 - 80, 190, 160, 50)
        pygame.draw.rect(self.screen, self.colors['button'], search_button)
        pygame.draw.rect(self.screen, self.colors['accent2'], search_button, 2)
        
        button_text = self.font.render("Search", True, self.colors['text'])
        button_rect = button_text.get_rect(center=search_button.center)
        self.screen.blit(button_text, button_rect)
        
        # Category filters
        categories = ["all", "title", "content", "wisdom", "tags"]
        category_width = 100
        total_width = category_width * len(categories)
        start_x = self.width // 2 - total_width // 2
        
        for i, category in enumerate(categories):
            x = start_x + i * category_width
            y = 260
            
            # Determine if this category is selected
            is_selected = category == self.search_category
            bg_color = self.colors['accent2'] if is_selected else self.colors['button']
            text_color = (0, 0, 0) if is_selected else self.colors['text']
            
            cat_rect = pygame.Rect(x, y, category_width - 10, 30)
            pygame.draw.rect(self.screen, bg_color, cat_rect)
            pygame.draw.rect(self.screen, self.colors['highlight'], cat_rect, 1)
            
            cat_text = self.font_small.render(category.capitalize(), True, text_color)
            cat_text_rect = cat_text.get_rect(center=cat_rect.center)
            self.screen.blit(cat_text, cat_text_rect)
        
        # Results
        if self.search_results:
            results_title = self.font.render(f"Found {len(self.search_results)} Records", True, self.colors['accent2'])
            results_rect = results_title.get_rect(center=(self.width // 2, 310))
            self.screen.blit(results_title, results_rect)
            
            # Draw scrollable results list
            result_height = 120
            start_y = 350 - self.scroll_offset
            
            for i, result in enumerate(self.search_results):
                y_pos = start_y + i * result_height
                
                # Skip records that are off-screen
                if y_pos + result_height < 310 or y_pos > self.height:
                    continue
                
                # Draw result panel
                result_rect = pygame.Rect(self.width // 2 - 400, y_pos, 800, result_height - 10)
                pygame.draw.rect(self.screen, (30, 30, 50), result_rect)
                pygame.draw.rect(self.screen, self.colors['highlight'], result_rect, 2)
                
                # Title
                title = self.font.render(result.get("title", "Untitled Record"), True, self.colors['accent1'])
                title_rect = title.get_rect(topleft=(result_rect.x + 20, result_rect.y + 15))
                self.screen.blit(title, title_rect)
                
                # Period and domain
                period_domain = None
                if "_period" in result and "_domain" in result:
                    period = result["_period"]
                    domain = result["_domain"]
                    
                    period_name = f"{period['name']} ({period['start_year']}-{period['end_year']})"
                    period_domain = self.font_small.render(
                        f"Period: {period_name} | Domain: {domain}", 
                        True, self.colors['accent2']
                    )
                elif "period" in result and "domain" in result:
                    period_domain = self.font_small.render(
                        f"Period: {result['period']} | Domain: {result['domain']}", 
                        True, self.colors['accent2']
                    )
                
                if period_domain:
                    period_domain_rect = period_domain.get_rect(topleft=(result_rect.x + 20, result_rect.y + 45))
                    self.screen.blit(period_domain, period_domain_rect)
                
                # Source
                source = self.font_small.render(
                    f"Source: {result.get('source_civilization', 'Unknown')}", 
                    True, self.colors['accent3']
                )
                source_rect = source.get_rect(topleft=(result_rect.x + 20, result_rect.y + 70))
                self.screen.blit(source, source_rect)
                
                # Preview of content/wisdom
                content = result.get("content", "")
                wisdom = result.get("wisdom", "")
                preview = content if content else wisdom
                preview = preview[:100] + "..." if len(preview) > 100 else preview
                
                if preview:
                    preview_text = self.font_small.render(preview, True, self.colors['text'])
                    preview_rect = preview_text.get_rect(topleft=(result_rect.x + 20, result_rect.y + 90))
                    self.screen.blit(preview_text, preview_rect)
            
            # Calculate max scroll
            total_height = len(self.search_results) * result_height
            self.max_scroll = max(0, total_height - (self.height - 350))
            
            # Draw scrollbar if needed
            if self.max_scroll > 0:
                scrollbar_height = max(50, (self.height - 350) * (self.height - 350) / total_height)
                scrollbar_pos = 350 + (self.height - 350 - scrollbar_height) * (self.scroll_offset / self.max_scroll)
                
                scrollbar_rect = pygame.Rect(self.width - 20, scrollbar_pos, 10, scrollbar_height)
                pygame.draw.rect(self.screen, self.colors['highlight'], scrollbar_rect)
        elif self.search_text:
            # No results message
            no_results = self.font.render("No records found matching your search criteria.", True, self.colors['text'])
            no_results_rect = no_results.get_rect(center=(self.width // 2, 400))
            self.screen.blit(no_results, no_results_rect)
            
            # Suggestions
            suggestions = self.font_small.render("Try different keywords or search in all categories.", True, self.colors['text'])
            suggestions_rect = suggestions.get_rect(center=(self.width // 2, 440))
            self.screen.blit(suggestions, suggestions_rect)
    
    def draw_notification(self):
        """Draw notification if active"""
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
        """Show a notification message"""
        self.notification = (message, color)
        self.notification_timer = time.time() + duration
    
    def handle_click(self, pos):
        """Handle mouse click events"""
        if self.view_mode == "main":
            # Check for search button click
            search_rect = pygame.Rect(self.width - 180, 60, 160, 40)
            if search_rect.collidepoint(pos):
                self.view_mode = "search"
                self.search_active = True
                self.search_text = ""
                self.search_results = []
                self.scroll_offset = 0
                return
            
            # Check for period selection
            timeline_y = 170
            for i, period in enumerate(self.time_periods):
                x_pos = 50 + (i + 0.5) * (self.width - 100) / len(self.time_periods)
                period_width = self.width // len(self.time_periods)
                
                select_rect = pygame.Rect(x_pos - period_width//2 + 20, timeline_y + 90, period_width - 40, 60)
                if select_rect.collidepoint(pos):
                    self.selected_period = period
                    self.view_mode = "period"
                    self.nav_history.append("main")
                    return
            
            # Check for domain selection (only first 12 visible on main page)
            domains_per_row = 4
            domain_width = self.width // domains_per_row - 20
            domain_height = 80
            
            for i, domain in enumerate(self.domains[:12]):
                row = i // domains_per_row
                col = i % domains_per_row
                
                x = col * (domain_width + 20) + 10
                y = 330 + row * (domain_height + 10)
                
                domain_rect = pygame.Rect(x, y, domain_width, domain_height)
                if domain_rect.collidepoint(pos):
                    # Let user select a period first
                    self.show_notification("Select a time period first to explore this domain", self.colors['warning'])
                    return
            
            # More domains button
            if len(self.domains) > 12:
                more_rect = pygame.Rect(self.width // 2 - 80, 690, 160, 50)
                if more_rect.collidepoint(pos):
                    self.show_notification("Select a time period first to view all domains", self.colors['warning'])
                    return
        
        elif self.view_mode == "period":
            # Check for back button
            back_rect = pygame.Rect(20, 20, 100, 40)
            if back_rect.collidepoint(pos):
                self.view_mode = "main"
                self.selected_period = None
                return
            
            # Check for domain selection
            domains_per_row = 3
            domain_width = self.width // domains_per_row - 40
            domain_height = 120
            
            period_info = self.load_period_info(self.selected_period)
            domain_counts = period_info.get("records_by_domain", {})
            sorted_domains = sorted(
                self.domains, 
                key=lambda d: domain_counts.get(d, 0), 
                reverse=True
            )
            
            for i, domain in enumerate(sorted_domains):
                row = i // domains_per_row
                col = i % domains_per_row
                
                x = col * (domain_width + 40) + 30
                y = 150 + row * (domain_height + 30)
                
                # Skip if below visible area
                if y > self.height - 30:
                    continue
                
                domain_rect = pygame.Rect(x, y, domain_width, domain_height)
                
                # Only allow clicking on domains with records
                record_count = domain_counts.get(domain, 0)
                if domain_rect.collidepoint(pos) and record_count > 0:
                    # Check if clicked on explore button
                    explore_rect = pygame.Rect(domain_rect.centerx - 60, domain_rect.bottom - 35, 120, 30)
                    
                    if explore_rect.collidepoint(pos) or not explore_rect.collidepoint(pos):
                        self.selected_domain = domain
                        self.view_mode = "domain"
                        self.records = self.load_domain_records(self.selected_period, domain)
                        self.scroll_offset = 0
                        self.nav_history.append("period")
                        return
        
        elif self.view_mode == "domain":
            # Check for back button
            back_rect = pygame.Rect(20, 20, 100, 40)
            if back_rect.collidepoint(pos):
                self.view_mode = "period"
                self.selected_domain = None
                self.records = []
                return
            
            # Check for record selection
            if self.records:
                record_height = 140
                start_y = 150 - self.scroll_offset
                
                for i, record in enumerate(self.records):
                    y_pos = start_y + i * record_height
                    
                    # Skip records that are off-screen
                    if y_pos + record_height < 0 or y_pos > self.height:
                        continue
                    
                    record_rect = pygame.Rect(self.width // 2 - 400, y_pos, 800, record_height - 20)
                    if record_rect.collidepoint(pos):
                        self.selected_record = record
                        self.view_mode = "record"
                        self.record_page = 0
                        self.nav_history.append("domain")
                        return
        
        elif self.view_mode == "record":
            # Check for back button
            back_rect = pygame.Rect(20, 20, 100, 40)
            if back_rect.collidepoint(pos):
                self.view_mode = "domain"
                self.selected_record = None
                return
            
            # Check for page navigation
            if "content" in self.selected_record:
                content = self.selected_record["content"]
                wrapped_content = textwrap.wrap(content, width=80)
                
                panel_rect = pygame.Rect(50, 80, self.width - 100, self.height - 100)
                content_rect = pygame.Rect(panel_rect.x + 30, panel_rect.bottom - 150, panel_rect.width - 60, 50)
                
                line_height = self.font_small.get_height()
                max_lines = content_rect.height // line_height - 1
                total_pages = (len(wrapped_content) + max_lines - 1) // max_lines
                
                if total_pages > 1:
                    page_rect = pygame.Rect(panel_rect.centerx - 50, panel_rect.bottom - 30, 100, 20)
                    
                    # Previous page button
                    if self.record_page > 0:
                        prev_rect = pygame.Rect(page_rect.left - 100, page_rect.top, 80, 30)
                        if prev_rect.collidepoint(pos):
                            self.record_page -= 1
                            return
                    
                    # Next page button
                    if self.record_page < total_pages - 1:
                        next_rect = pygame.Rect(page_rect.right + 20, page_rect.top, 80, 30)
                        if next_rect.collidepoint(pos):
                            self.record_page += 1
                            return
            
            # Check for related record clicks
            if "related_records" in self.selected_record and self.selected_record["related_records"]:
                related_rect = pygame.Rect(panel_rect.x + 30, panel_rect.bottom - 50, 200, 30)
                
                x_pos = related_rect.right + 20
                for i, related in enumerate(self.selected_record["related_records"][:3]):
                    related_text_rect = pygame.Rect(x_pos, related_rect.top - 5, 150, 30)
                    
                    if related_text_rect.collidepoint(pos):
                        # Load the related record
                        related_record = self.load_record(related.get("id"))
                        if related_record:
                            self.selected_record = related_record
                            self.record_page = 0
                            return
                        else:
                            self.show_notification("Could not load related record", self.colors['warning'])
                            return
                    
                    x_pos += 160
        
        elif self.view_mode == "search":
            # Check for back button
            back_rect = pygame.Rect(20, 20, 100, 40)
            if back_rect.collidepoint(pos):
                if self.nav_history:
                    self.view_mode = self.nav_history.pop()
                else:
                    self.view_mode = "main"
                self.search_active = False
                return
            
            # Check for search box
            search_rect = pygame.Rect(self.width // 2 - 300, 120, 600, 50)
            if search_rect.collidepoint(pos):
                self.search_active = True
                return
            
            # Check for search button
            search_button = pygame.Rect(self.width // 2 - 80, 190, 160, 50)
            if search_button.collidepoint(pos):
                if self.search_text.strip():
                    self.search_results = self.search_archives(self.search_text, self.search_category)
                    self.scroll_offset = 0
                    self.search_active = False
                    
                    if self.search_results:
                        self.show_notification(f"Found {len(self.search_results)} matching records", self.colors['success'])
                    else:
                        self.show_notification("No matching records found", self.colors['warning'])
                else:
                    self.show_notification("Enter a search term", self.colors['warning'])
                return
            
            # Check for category filters
            categories = ["all", "title", "content", "wisdom", "tags"]
            category_width = 100
            total_width = category_width * len(categories)
            start_x = self.width // 2 - total_width // 2
            
            for i, category in enumerate(categories):
                x = start_x + i * category_