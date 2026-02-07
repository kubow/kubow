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

# Define all chart data matching Mermaid charts from README.md
charts_data = {
    'frontend': {
        'title': 'Frontend Technologies',
        'filename': 'radar_chart_frontend',
        'data': {
            'HTML5': {'value': 80, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg'},
            'CSS': {'value': 60, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg'},
            'JavaScript': {'value': 65, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg'},
            'TypeScript': {'value': 45, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg'},
            'React': {'value': 60, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg'},
            'Vue': {'value': 60, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg'},
            'Svelte': {'value': 70, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/svelte/svelte-original.svg'},
            'Tailwind': {'value': 50, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-original.svg'},
            'Flask': {'value': 65, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg'},
            'Streamlit': {'value': 70, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/streamlit/streamlit-original.svg'}
        }
    },
    'backend': {
        'title': 'Backend Languages',
        'filename': 'radar_chart_backend',
        'data': {
            'Linux Shell': {'value': 65, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg'},
            'Windows Shell': {'value': 75, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/windows8/windows8-original.svg'},
            'Python': {'value': 70, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg'},
            'Rust': {'value': 40, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rust/rust-original.svg'},
            'Java Based': {'value': 25, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg'},
            'C Based': {'value': 20, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/c/c-original.svg'}
        }
    },
    'data': {
        'title': 'Data Related Stack',
        'filename': 'radar_chart_data',
        'data': {
            'SQLite': {'value': 85, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg'},
            'PostgreSQL': {'value': 80, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg'},
            'DuckDB': {'value': 75, 'icon': 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/duckdb.svg'},
            'SAP': {'value': 50, 'icon': 'https://www.vectorlogo.zone/logos/sap/sap-ar21.svg'},
            'Oracle': {'value': 40, 'icon': 'https://www.vectorlogo.zone/logos/oracle/oracle-ar21.svg'},
            'Microsoft': {'value': 65, 'icon': 'https://www.vectorlogo.zone/logos/microsoft/microsoft-ar21.svg'},
            'Snowflake': {'value': 70, 'icon': 'https://www.vectorlogo.zone/logos/snowflake/snowflake-ar21.svg'},
            'Databricks': {'value': 65, 'icon': 'https://www.vectorlogo.zone/logos/databricks/databricks-ar21.svg'},
            'Analytics': {'value': 90, 'icon': 'https://www.gooddata.com/img/generic/logo-gd-b.svg'},
            'Data Pipeline': {'value': 80, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apacheairflow/apacheairflow-original.svg'},
            'Data Modelling': {'value': 70, 'icon': None}
        }
    },
    'map': {
        'title': 'Map Related',
        'filename': 'radar_chart_map',
        'data': {
            'ArcGIS': {'value': 75, 'icon': 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/arcgis.svg'},
            'OSGeo': {'value': 70, 'icon': 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/osgeo.svg'},
            'QGIS': {'value': 80, 'icon': 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/qgis.svg'},
            'DHI MIKE': {'value': 85, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg'},
            'EpaNET': {'value': 85, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg'},
            'Map Services': {'value': 70, 'icon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mapbox/mapbox-original.svg'},
            'Embedded Maps': {'value': 70, 'icon': 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/openstreetmap.svg'},
            'CAD': {'value': 50, 'icon': 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/autodesk.svg'}
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
    
    # Set text labels for each category - but don't display them (we use icons/text at end of radials)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])  # Remove degree/angle labels at outside border
    
    # Set y-axis limits to max at 110 (where icons are positioned)
    ax.set_ylim(0, 110)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=9)
    ax.grid(True, linestyle='--', linewidth=0.5)
    
    # Add title
    plt.title(title, size=16, fontweight='bold', pad=30)
    
    # Add text labels first (these work reliably with polar coordinates)
    icon_values = values[:-1]  # Get values without the closing point
    
    for i, (category, angle, value) in enumerate(zip(categories, angles[:-1], icon_values)):
        # Position slightly beyond the data point value
        label_radius = value + 15  # Offset to place label at end of radial
        
        # Add text label at the end of the radial line
        ax.text(angle, label_radius, category, 
               ha='center', va='center',
               fontsize=9, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Draw the plot to ensure transforms are ready
    plt.tight_layout()
    fig.canvas.draw()
    
    # Now add icons - they need the plot to be drawn first for correct transforms
    for i, (category, angle, value) in enumerate(zip(categories, angles[:-1], icon_values)):
        icon_radius = 110   # Position icon at radius=110 on each radial
        
        # Add icon if available - position it on the radial line
        if icons[category]:
            try:
                icon_img = load_icon_from_url(icons[category], size=60)  # Half size (60px)
                icon_img_pil = Image.fromarray(icon_img)
                
                # Create offset image
                zoom_factor = 0.5  # Half zoom to match half size
                imagebox = OffsetImage(icon_img_pil, zoom=zoom_factor)
                
                # For polar plots, transData expects polar coordinates (angle, radius)
                # NOT cartesian! Use angle and radius directly like ax.text does
                ab = AnnotationBbox(imagebox, (angle, icon_radius),
                                    xycoords=ax.transData,
                                    frameon=False, pad=0,
                                    box_alignment=(0.5, 0.5),
                                    zorder=10)  # Ensure icons are on top
                ax.add_artist(ab)
            except Exception as e:
                print(f"Warning: Could not add icon for {category}: {e}")
    
    # Save as SVG only
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
