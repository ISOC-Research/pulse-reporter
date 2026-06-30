import re
import glob

def quote_xaxis(m):
    prefix = m.group(1)
    items = [x.strip() for x in m.group(2).split(',')]
    quoted = []
    for x in items:
        clean_x = x.strip('"\'')
        # Remove parentheses content to save space (e.g. ASNs, "(Overall)")
        clean_x = re.sub(r'\s*\(.*?\)', '', clean_x)
        # Truncate if still too long
        if len(clean_x) > 15:
            clean_x = clean_x[:13] + '..'
        quoted.append(f'"{clean_x}"')
    return prefix + '[' + ', '.join(quoted) + ']'

def fix_xychart(match):
    block = match.group(0)
    return re.sub(r'(x-axis.*?)(?:\[(.*?)\])', quote_xaxis, block)

def fix_pie_sum(match):
    block = match.group(0)
    lines = block.split('\n')
    parsed = []
    total = 0.0
    lines_to_keep = []
    
    for i, line in enumerate(lines):
        m = re.search(r'(".*?")\s*:\s*([\d\.]+)', line)
        if m:
            val = float(m.group(2))
            if val < 0.5:
                continue
            parsed.append((len(lines_to_keep), val, line, m.group(1)))
            total += val
            lines_to_keep.append(line)
        else:
            lines_to_keep.append(line)
            
    if parsed and abs(total - 100.0) > 0.001 and total > 0:
        largest_idx = max(range(len(parsed)), key=lambda x: parsed[x][1])
        idx_in_lines, val, orig_line, orig_label = parsed[largest_idx]
        diff = 100.0 - total
        new_val = round(val + diff, 2)
        parsed[largest_idx] = (idx_in_lines, new_val, orig_line, orig_label)
        lines_to_keep[idx_in_lines] = re.sub(r'[\d\.]+\s*$', str(new_val), orig_line)
        
    for idx_in_lines, val, orig_line, orig_label in parsed:
        clean_label = re.sub(r'\s*\([\d\.]+\s*%?\)', '', orig_label.strip('"'))
        new_label = f'"{clean_label} ({val:g}%)"'
        lines_to_keep[idx_in_lines] = re.sub(r'".*?"', new_label, lines_to_keep[idx_in_lines], count=1)
        
    return '\n'.join(lines_to_keep)

for html_path in glob.glob(r'C:\CollegeWork\SummerInternship2\ISOC_Workspace\pulse-reporter\reports\*.html'):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = re.sub(r'xychart-beta.*?(?:</div>|</pre>)', fix_xychart, html, flags=re.DOTALL)
    html = re.sub(r'pie title.*?(?:</div>|</pre>)', fix_pie_sum, html, flags=re.DOTALL)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed {html_path}")
