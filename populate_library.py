import os
import json
import time
from datetime import datetime, timedelta

def populate_cosmic_library():
    library_path = "cosmic_data"
    
    # Ensure the library path exists
    if not os.path.exists(library_path):
        os.makedirs(library_path)
    
    categories = [
        "Universal Knowledge",
        "Cosmic Events",
        "Soul Records",
        "Planetary Wisdom",
        "Consciousness Patterns",
        "Vibrational Data",
        "Timeline Recordings"
    ]
    
    # Sample cosmic data to populate the library
    cosmic_data = {
        "Universal Knowledge": [
            {
                "title": "The Cosmic Web of Consciousness",
                "content": "The universe is interconnected through a vast web of consciousness that transcends physical space. Every thought and action ripples through this field, creating patterns that can be accessed through deep meditative states."
            },
            {
                "title": "Principles of Universal Harmony",
                "content": "Seven fundamental vibrational patterns form the basis of all reality. These patterns manifest across all scales, from quantum fields to galactic structures, creating a harmonic resonance that maintains cosmic balance."
            }
        ],
        "Cosmic Events": [
            {
                "title": "The Great Celestial Alignment of 2026",
                "content": "A rare alignment of planetary bodies will create a unique energy corridor between Earth and the galactic center, opening a window for heightened consciousness and spiritual awakening."
            },
            {
                "title": "Photonic Light Waves of 2024-2027",
                "content": "Increasing photonic light waves from the central sun are changing Earth's electromagnetic field, affecting human DNA and accelerating the awakening process across the planet."
            }
        ],
        "Soul Records": [
            {
                "title": "Soul Group Connections",
                "content": "Soul families or groups incarnate together across multiple lifetimes to work on shared karmic patterns and evolutionary goals. Recognition between members often comes through intuitive knowing rather than logical understanding."
            },
            {
                "title": "Accessing Past Life Information",
                "content": "The Akashic field contains complete records of all experiences across all timelines. Through specific meditation techniques, individuals can access relevant past life information that supports their current growth."
            }
        ],
        "Planetary Wisdom": [
            {
                "title": "Earth's Energetic Grid System",
                "content": "The planet maintains a complex energetic grid with key nodal points at sacred sites around the world. These points act as transmitters and receivers for cosmic information and can be used for planetary healing."
            },
            {
                "title": "Crystal Consciousness Networks",
                "content": "Earth's crystal deposits form a sophisticated communication network that stores and processes information. Ancient civilizations understood how to interface with this network to access planetary wisdom."
            }
        ],
        "Consciousness Patterns": [
            {
                "title": "The Seven Stages of Consciousness Evolution",
                "content": "Consciousness evolves through seven distinct stages, each with its own vibrational signature and perceptual framework. Understanding these stages helps navigate personal and collective evolutionary processes."
            },
            {
                "title": "Quantum Consciousness Fields",
                "content": "The observer effect in quantum physics demonstrates how consciousness influences reality at the most fundamental level. By directing focused awareness, individuals can influence probability fields and manifest desired outcomes."
            }
        ],
        "Vibrational Data": [
            {
                "title": "Sound Healing Frequencies",
                "content": "Specific sound frequencies can reorganize molecular structures and restore harmonic balance to biological systems. Ancient solfeggio frequencies (396Hz, 417Hz, 528Hz, etc.) have powerful healing effects on mind, body and spirit."
            },
            {
                "title": "Color Frequencies and Consciousness",
                "content": "Each color vibration affects different aspects of human consciousness and energy systems. Working with specific color frequencies can balance chakras and enhance spiritual perception."
            }
        ],
        "Timeline Recordings": [
            {
                "title": "Accessing Parallel Timelines",
                "content": "Multiple timelines exist simultaneously in quantum fields. Through specific consciousness techniques, it's possible to perceive and even influence events across parallel reality streams."
            },
            {
                "title": "Timeline Convergence Points",
                "content": "Certain moments represent nexus points where multiple timelines converge, creating windows of opportunity for significant change. Recognizing these points allows for conscious participation in evolutionary leaps."
            }
        ]
    }
    
    # Create folders and populate with data
    for category in categories:
        category_folder = os.path.join(library_path, category.replace(" ", "_"))
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)
            
        # Add sample data for this category
        if category in cosmic_data:
            for idx, entry in enumerate(cosmic_data[category]):
                # Create record with random dates in past month
                days_ago = 30 - idx * 3  # Space out the entries
                record_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
                
                record = {
                    "title": entry["title"],
                    "content": entry["content"],
                    "date": record_date,
                    "user": "cosmic_librarian"
                }
                
                # Save to file
                timestamp = int(time.time()) - (days_ago * 86400)  # Approximate timestamp
                filename = os.path.join(category_folder, f"{timestamp}.json")
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(record, f, ensure_ascii=False, indent=2)
                    
    print("Cosmic library has been populated with initial data.")
    print(f"Created {sum(len(entries) for entries in cosmic_data.values())} cosmic records across {len(categories)} categories.")

if __name__ == "__main__":
    populate_cosmic_library()