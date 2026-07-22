from pathlib import Path
p=Path('renderer/index.html')
s=p.read_text()
old='''      <div class="form-group">
        <label>Dán link bài báo hoặc nhập danh sách tiêu đề (mỗi dòng 1 tiêu đề)</label>
        <input type="text" id="articleUrl" placeholder="Dán link bài báo để lấy nội dung..." style="margin-bottom:8px;">
        <button class="secondary" style="margin-bottom:8px" onclick="fetchArticleIntoTopic()">🔗 Lấy nội dung từ link</button>
        <textarea id="topic" rows="5" placeholder="Dán link bài báo ở trên hoặc nhập tiêu đề/nội dung mỗi dòng..."></textarea>
      </div>'''
new='''      <div class="form-group">
        <label>Nhập danh sách tiêu đề / chủ đề (mỗi dòng 1 tiêu đề)</label>
        <textarea id="topic" rows="5" placeholder="Nhập tiêu đề hoặc chủ đề mỗi dòng..."></textarea>
      </div>'''
s=s.replace(old,new)
old='''              <button class="btn-primary" onclick="regenerateActiveTitle()">🔄 Tạo lại tiêu đề này</button>
              <button class="secondary" onclick="copyOutput('outputTab2')">📋 Copy prompt</button>
              <button class="secondary" onclick="downloadActiveResult()">💾 Tải .txt</button>
              <button class="secondary" onclick="downloadAllResults()">📦 Tải toàn bộ nội dung</button>'''
new='''              <button class="btn-primary" onclick="regenerateActiveTitle()">🔄 Tạo lại</button>
              <button class="secondary" onclick="copyOutput('outputTab2')">📋 Copy</button>
              <button class="secondary" onclick="downloadActiveResult()">💾 Tải xuống</button>
              <button class="secondary" onclick="downloadAllResults()">📦 Tải tất cả</button>'''
s=s.replace(old,new)
p.write_text(s)
