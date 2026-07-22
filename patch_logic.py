from pathlib import Path
p=Path('renderer/app.js')
s=p.read_text()
s=s.replace("""function saveLengthSettings() {
  const minEl = document.getElementById('minChars');
  const maxEl = document.getElementById('maxChars');
  if (minEl) localStorage.setItem('aiContentMinChars', minEl.value.trim());
  if (maxEl) localStorage.setItem('aiContentMaxChars', maxEl.value.trim());
}""", """function saveLengthSettings() {
  const minEl = document.getElementById('minChars');
  const maxEl = document.getElementById('maxChars');
  const rMin = document.getElementById('rewriteMinChars');
  const rMax = document.getElementById('rewriteMaxChars');
  if (minEl) localStorage.setItem('aiContentMinChars', minEl.value.trim());
  if (maxEl) localStorage.setItem('aiContentMaxChars', maxEl.value.trim());
  if (rMin) localStorage.setItem('aiRewriteMinChars', rMin.value.trim());
  if (rMax) localStorage.setItem('aiRewriteMaxChars', rMax.value.trim());
}""")
start=s.index('async function rewriteContent() {')
end=s.index('\n}', start)+2
new="""async function rewriteContent() {
  const bot = config.bots[0];
  if (!bot) return alert('Chưa có cấu hình API/Gemini. Vào Cấu hình Bot lưu API trước.');

  const original = document.getElementById('originalContent').value.trim();
  if (!original) return alert('Chưa có nội dung để viết lại.');

  const req = document.getElementById('rewriteRequirements').value.trim();
  const rMinRaw = document.getElementById('rewriteMinChars')?.value?.trim() || '';
  const rMaxRaw = document.getElementById('rewriteMaxChars')?.value?.trim() || '';
  const min = rMinRaw ? Number(rMinRaw) : 0;
  const max = rMaxRaw ? Number(rMaxRaw) : 0;
  saveLengthSettings();

  const lengthTarget = pickLengthTarget(min, max);
  const rewriteLengthInstruction = buildLengthInstruction(min, max, lengthTarget, true);
  setOutput('outputTab3', 'Đang viết lại...');

  const prompt = `Bạn là biên tập viên chuyên nghiệp. Hãy VIẾT LẠI nội dung dưới đây thành một bài mới hay hơn bản gốc, chuyên sâu hơn, mạch lạc hơn, giàu thông tin hơn.

YÊU CẦU BẮT BUỘC:
- Viết đúng theo yêu cầu/theme: ${req || 'viết lại tự nhiên, chuyên sâu, hấp dẫn, dễ đọc'}.
- Giữ đúng ý chính và dữ kiện quan trọng của bản gốc, không bịa thông tin sai.
- Mở rộng phân tích, thêm ngữ cảnh, giải thích sâu hơn, câu văn hay hơn bản gốc.
- Không viết ngắn cụt. Không tóm tắt.
- ${rewriteLengthInstruction}
- Nếu người dùng nhập số ký tự, phải bám sát số đó. Không tự ý rút ngắn.
- Trả về DUY NHẤT nội dung đã viết lại. Không tiêu đề phụ thừa, không ghi chú, không giải thích, không markdown.

NỘI DUNG GỐC:
${original}`;

  try {
    const data = await window.api.callApi({ bot, prompt });
    if (data.error) throw new Error(JSON.stringify(data.error, null, 2));
    let text = cleanPromptText(data?.choices?.[0]?.message?.content || data?.candidates?.[0]?.content?.parts?.[0]?.text || '');

    let requiredMin = lengthTarget ? Math.floor(lengthTarget * 0.95) : 0;
    if (min > 0) requiredMin = Math.max(requiredMin, min);
    if (max > 0 && requiredMin >= max) requiredMin = Math.max(1, max - 1);

    let attempts = 0;
    while (requiredMin && text.length < requiredMin && attempts < 6) {
      attempts++;
      const remaining = requiredMin - text.length;
      const extendPrompt = `Bài viết lại hiện còn thiếu ký tự.
Độ dài hiện tại: ${text.length} ký tự.
Cần tối thiểu: ${requiredMin} ký tự.
Hãy viết tiếp tự nhiên, chuyên sâu hơn, thêm phân tích/ngữ cảnh liên quan, không lặp lại ý đã có.
Chỉ trả về phần viết tiếp, khoảng ${remaining} ký tự hoặc hơn một chút.
${max > 0 ? `Tổng cuối cùng không được vượt quá ${max} ký tự.` : ''}

NỘI DUNG ĐÃ CÓ:
${text}`;
      const moreData = await window.api.callApi({ bot, prompt: extendPrompt });
      if (moreData.error) throw new Error(JSON.stringify(moreData.error, null, 2));
      const moreText = cleanPromptText(moreData?.choices?.[0]?.message?.content || moreData?.candidates?.[0]?.content?.parts?.[0]?.text || '');
      if (!moreText) break;
      text = cleanPromptText(text + ' ' + moreText);
      if (max > 0 && text.length >= max) {
        text = cleanPromptText(normalizeToRange(text, min, max));
        break;
      }
    }

    text = cleanPromptText(normalizeToRange(text, min, max));
    setOutput('outputTab3', text);
  } catch (err) {
    setOutput('outputTab3', `[LỖI]: ${err.message}`);
  }
}"""
s=s[:start]+new+s[end:]
p.write_text(s)
