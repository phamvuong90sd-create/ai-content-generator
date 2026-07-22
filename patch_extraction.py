from pathlib import Path
p=Path('main.js')
s=p.read_text()
old='''    const article = html.match(/<article[\s\S]*?<\/article>/i);
    const main = html.match(/<main[\s\S]*?<\/main>/i);
    if (article) body = article[0]; else if (main) body = main[0];
    let roughText = body
      .replace(/<script[\s\S]*?<\/script>/gi, ' ')
      .replace(/<style[\s\S]*?<\/style>/gi, ' ')
      .replace(/<nav[\s\S]*?<\/nav>/gi, ' ')
      .replace(/<header[\s\S]*?<\/header>/gi, ' ')
      .replace(/<footer[\s\S]*?<\/footer>/gi, ' ')
      .replace(/<aside[\s\S]*?<\/aside>/gi, ' ')
      .replace(/<img[^>]*>/gi, ' ')
      .replace(/<h1[\s\S]*?<\/h1>/gi, ' ')
      .replace(/<h2[\s\S]*?<\/h2>/gi, ' ')
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<\/p>/gi, '\n')
      .replace(/<[^>]+>/g, ' ')'''
new='''    const article = html.match(/<article[\s\S]*?<\/article>/i);
    const main = html.match(/<main[\s\S]*?<\/main>/i);
    if (article) body = article[0]; else if (main) body = main[0];
    let roughText = body
      .replace(/<script[\s\S]*?<\/script>/gi, ' ')
      .replace(/<style[\s\S]*?<\/style>/gi, ' ')
      .replace(/<nav[\s\S]*?<\/nav>/gi, ' ')
      .replace(/<header[\s\S]*?<\/header>/gi, ' ')
      .replace(/<footer[\s\S]*?<\/footer>/gi, ' ')
      .replace(/<aside[\s\S]*?<\/aside>/gi, ' ')
      .replace(/<img[^>]*>/gi, ' ')
      .replace(/<figure[\s\S]*?<\/figure>/gi, ' ')
      .replace(/<figcaption[\s\S]*?<\/figcaption>/gi, ' ')
      .replace(/<div class="[^"]*?(banner|ads|sidebar|comment|related)[^"]*?"[\s\S]*?<\/div>/gi, ' ')
      .replace(/<h1[\s\S]*?<\/h1>/gi, ' ')
      .replace(/<h2[\s\S]*?<\/h2>/gi, ' ')
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<\/p>/gi, '\n')
      .replace(/<[^>]+>/g, ' ')'''
s=s.replace(old,new)
p.write_text(s)
