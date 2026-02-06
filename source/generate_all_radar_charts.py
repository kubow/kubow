"""
Script to generate all 4 radar charts with icons instead of text labels:
1. Frontend Technologies
2. Backend Languages
3. Data Related Stack
4. Map Related

Usage:
    python generate_all_radar_charts.py

Requirements:
    pip install matplotlib numpy pillow requests cairosvg
"""

import matplotlib.pyplot as plt
import numpy as np
from math import pi
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import requests
from io import BytesIO
import os

# Define all chart data with icon URLs - customize values (0-100 scale) as needed
charts_data = {
    'frontend': {
        'title': 'Frontend Technologies',
        'filename': 'radar_chart_frontend',
        'data': {
            'HTML5': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg'},
            'CSS': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg'},
            'JavaScript': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg'},
            'TypeScript': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg'},
            'React': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg'},
            'Vue': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg'},
            'Svelte': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/svelte/svelte-original.svg'},
            'Tailwind': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-original.svg'}
        }
    },
    'backend': {
        'title': 'Backend Languages',
        'filename': 'radar_chart_backend',
        'data': {
            'Python': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg'},
            'JavaScript': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg'},
            'Flask': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg'},
            'Streamlit': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/streamlit/streamlit-original.svg'}
        }
    },
    'data': {
        'title': 'Data Related Stack',
        'filename': 'radar_chart_data',
        'data': {
            'SQLite': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg'},
            'PostgreSQL': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg'},
            'DuckDB': {'value': 50, 'icon': 'https://duckdb.org/images/duckdb_logo_icon.svg'},
            'SAP': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sap/sap-original.svg'},
            'GoodData': {'value': 50, 'icon': 'https://www.gooddata.com/img/generic/logo-gd-b.svg'},
            'PowerBI': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/powerbi/powerbi-original.svg'},
            'Jupyter': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jupyter/jupyter-original.svg'}
        }
    },
    'map': {
        'title': 'Map Related',
        'filename': 'radar_chart_map',
        'data': {
            'OpenLayers': {'value': 50, 'icon': 'https://openlayers.org/theme/img/logo-70x70.png'},
            'Leaflet': {'value': 50, 'icon': 'https://leafletjs.com/docs/images/logo.png'},
            'ArcGIS': {'value': 50, 'icon': 'https://www.arcgis.com/about/graphics/logo-arcgis.png'},
            'Mapbox': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mapbox/mapbox-original.svg'},
            'QGIS': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/qgis/qgis-original.svg'}
        }
    }
}

def load_icon_from_url(url, size=40):
    """Load icon from URL and resize it - handles both PNG and SVG using cairosvg if available"""
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        content = response.content
        
        # Check if it's SVG
        if url.endswith('.svg') or b'<svg' in content[:100]:
            # Try to use cairosvg to convert SVG to PNG
            try:
                import cairosvg
                png_data = cairosvg.svg2png(bytestring=content, output_width=size*2, output_height=size*2)
                img = Image.open(BytesIO(png_data))
            except ImportError:
                # Fallback: try to use svglib if available
                try:
                    from svglib.svglib import svg2rlg
                    from reportlab.graphics import renderPM
                    drawing = svg2rlg(BytesIO(content))
                    png_data = renderPM.drawToString(drawing, fmt='PNG')
                    img = Image.open(BytesIO(png_data))
                except ImportError:
                    # Last resort: return placeholder and print message
                    print(f"Note: SVG support requires 'cairosvg' or 'svglib'. Install with: pip install cairosvg")
                    return np.ones((size, size, 3), dtype=np.uint8) * 200
        else:
            # It's a regular image (PNG, JPG, etc.)
            img = Image.open(BytesIO(content))
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
            
        img.thumbnail((size, size), Image.Resampling.LANCZOS)
        return np.array(img)
    except Exception as e:
        print(f"Warning: Could not load icon from {url}: {e}")
        # Return a simple placeholder
        return np.ones((size, size, 3), dtype=np.uint8) * 200

def generate_radar_chart(data, title, filename):
    """Generate a single radar chart with icons"""
    # Prepare data - extract values and icons
    categories = list(data.keys())
    values = [data[cat]['value'] if isinstance(data[cat], dict) else data[cat] for cat in categories]
    icons = {cat: data[cat]['icon'] if isinstance(data[cat], dict) and 'icon' in data[cat] else None 
             for cat in categories}
    
    n_categories = len(categories)
    
    # Compute angle for each category
    angles = [n / float(n_categories) * 2 * pi for n in range(n_categories)]
    angles += angles[:1]  # Complete the circle
    
    # Add first value at the end to close the chart
    values += values[:1]
    
    # Create the plot - larger figure to accommodate bigger icons
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))
    
    # Plot the data (without markers at the end, we'll use icons instead)
    ax.plot(angles, values, '-', linewidth=2, color='steelblue')
    ax.fill(angles, values, alpha=0.3, color='steelblue')
    
    # Remove text labels - we'll use icons instead
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])  # Remove text labels
    
    # Set y-axis limits and labels - increase to make room for larger icons
    max_value = max(values[:-1]) if values else 100
    ax.set_ylim(0, max(120, max_value + 30))  # Extra space for icons
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=9)
    ax.grid(True, linestyle='--', linewidth=0.5)
    
    # Add icons at the end of each radial line (at the value position)
    icon_size = 80  # Much larger icons
    icon_values = values[:-1]  # Get values without the closing point
    
    for i, (category, angle, value) in enumerate(zip(categories, angles[:-1], icon_values)):
        if icons[category]:
            try:
                icon_img = load_icon_from_url(icons[category], size=icon_size)
                # Convert to image for OffsetImage
                icon_img_pil = Image.fromarray(icon_img)
                
                # Create offset image - larger zoom for bigger icons
                imagebox = OffsetImage(icon_img_pil, zoom=0.8)
                
                # Calculate the position slightly beyond the value to place icon at the end of radial line
                icon_radius = value + 10  # Offset to place icon just beyond the data point
                
                # For polar plots, use the polar coordinate system directly
                # The issue is that AnnotationBbox doesn't perfectly center on polar axes
                # We'll use polar coordinates and rely on box_alignment
                ab = AnnotationBbox(imagebox, (angle, icon_radius), 
                                    xycoords=('polar', 'data'),
                                    frameon=False, pad=0,
                                    box_alignment=(0.5, 0.5))
                ax.add_artist(ab)
                
                # Also draw a small marker at the exact data point to help with alignment
                ax.plot([angle], [value], 'o', color='steelblue', markersize=4, zorder=5)
            except Exception as e:
                print(f"Warning: Could not add icon for {category}: {e}")
                # Fallback to text if icon fails
                ax.text(angle, value, category[:8], ha='center', va='center',
                       fontsize=8, fontweight='bold')
        else:
            # Fallback to text if no icon URL
            ax.text(angle, value, category[:8], ha='center', va='center',
                   fontsize=8, fontweight='bold')
    
    # Add title
    plt.title(title, size=16, fontweight='bold', pad=30)
    
    # Save as SVG only
    plt.tight_layout()
    svg_path = f'{filename}.svg'
    plt.savefig(svg_path, format='svg', bbox_inches='tight', facecolor='white')
    plt.close()  # Close the figure to free memory
    
    return svg_path

# Generate all charts
print("Generating radar charts...\n")
generated_files = []

for chart_key, chart_info in charts_data.items():
    svg_path = generate_radar_chart(
        chart_info['data'],
        chart_info['title'],
        chart_info['filename']
    )
    generated_files.append((chart_info['title'], chart_info['filename']))
    print(f"✓ {chart_info['title']} saved as '{svg_path}'")

print("\n" + "="*60)
print("All charts generated successfully!")
print("\nTo embed in your README.md, use:")
print("\n### Frontend Technologies")
print("![Frontend Technologies](source/radar_chart_frontend.svg)")
print("\n### Backend Languages")
print("![Backend Languages](source/radar_chart_backend.svg)")
print("\n### Data Related Stack")
print("![Data Related Stack](source/radar_chart_data.svg)")
print("\n### Map Related")
print("![Map Related](source/radar_chart_map.svg)")
