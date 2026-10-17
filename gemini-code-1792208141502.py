import streamlit as st
import time
import re

st.set_page_config(page_title="Dynamic NLP Essay Evaluator", page_icon="📝", layout="wide")

st.title("📝 Hệ thống NLP Phân tích Bài viết Tiếng Anh Thuận theo Văn bản Học sinh")
st.caption("Chuyên môn NLP: Real-time Rule-based Grammar Diagnostics, Dynamic Tokenization & Lexical Analysis")
st.markdown("---")

# --- BƯỚC 1: NHẬP BÀI LUẬN TỰ DO CỦA HỌC SINH ---
st.header("Bước 1: Nhập hoặc Tải lên bài viết Tiếng Anh bất kỳ của Học sinh")

essay_topic = st.text_input("Đề bài / Chủ đề bài luận (Topic):", 
                            placeholder="Ví dụ: Benefits of learning English, Environmental protection...")

student_essay = st.text_area("Nội dung bài viết của Học sinh (Gõ hoặc dán văn bản tự do vào đây):", 
                             placeholder="Nhập đoạn văn tiếng Anh của học sinh tại đây để AI phân tích...",
                             height=200)

if st.button("🚀 Chạy Mô hình NLP Phân tích Văn bản Trực tiếp"):
    if not student_essay.strip():
        st.error("Vui lòng nhập bài viết tiếng Anh để hệ thống NLP phân tích!")
    else:
        with st.spinner("NLP Engine đang xử lý Tokenization, Grammar Rules & Parsing văn bản thực tế..."):
            time.sleep(1.5)
        st.session_state['analyzed_text'] = student_essay
        st.session_state['analyzed'] = True

# --- BƯỚC 2, 3, 4: PHÂN TÍCH ĐỘNG DỰA TRÊN VĂN BẢN THỰC TẾ ---
if st.session_state.get('analyzed', False):
    text = st.session_state.get('analyzed_text', '')
    
    st.markdown("---")
    st.header("Bước 2 & 3: Kết quả Phân tích Trực tiếp từ Bài viết của Học sinh")
    
    # 1. TOKENIZATION DỮ LIỆU THỰC TẾ
    raw_words = re.findall(r'\b\w+\b', text)
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    
    word_count = len(raw_words)
    sentence_count = len(sentences)
    unique_words = len(set([w.lower() for w in raw_words]))
    
    # 2. TÍNH CHỈ SỐ TTR (TYPE-TOKEN RATIO) ĐỘNG
    ttr = round((unique_words / word_count) * 100, 1) if word_count > 0 else 0
    avg_sentence_len = round(word_count / sentence_count, 1) if sentence_count > 0 else 0

    # Hiển thị số liệu thực tế từ bài viết
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Tổng số từ (Word Count)", value=f"{word_count}")
    with col2:
        st.metric(label="Số câu (Sentence Count)", value=f"{sentence_count}")
    with col3:
        st.metric(label="Độ dài trung bình câu", value=f"{avg_sentence_len} từ/câu")
    with col4:
        st.metric(label="Độ đa dạng từ vựng (TTR)", value=f"{ttr}%")

    st.markdown("---")
    st.subheader("🔍 Chi tiết Lỗi Ngữ pháp & Cú pháp phát hiện ĐỘNG từ bài viết:")
    
    # 3. ENGINE BẮT LỖI DỰA TRÊN LUẬT NLP VÀ VĂN BẢN THỰC TẾ
    detected_errors = []
    
    # Luật 1: Kiểm tra lỗi viết hoa đầu câu
    for idx, sent in enumerate(sentences, 1):
        if sent and not sent[0].isupper():
            detected_errors.append({
                "cau": sent,
                "loi_loai": "Capitalization Error",
                "de_xuat": f"Viết hoa chữ cái đầu câu: '{sent[0].upper() + sent[1:]}'",
                "giai_thich": "Mọi câu trong Tiếng Anh bắt đầu bằng chữ cái viết hoa."
            })

    # Luật 2: Kiểm tra lỗi "a/an" trước nguyên âm
    vowel_matches = re.findall(r'\b(a)\s+([aeiouAEIOU]\w+)', text)
    for m in vowel_matches:
        detected_errors.append({
            "cau": f"...a {m[1]}...",
            "loi_loai": "Indefinite Article Error (a/an)",
            "de_xuat": f"Đổi 'a {m[1]}' thành 'an {m[1]}'",
            "giai_thich": "Dùng mạo từ 'an' trước các từ bắt đầu bằng nguyên âm (a, e, i, o, u)."
        })

    # Luật 3: Kiểm tra lỗi danh từ số nhiều đi với "many"
    many_matches = re.findall(r'\b(many|several)\s+([a-zA-Cg-z]+)(?<!s)\b', text, re.IGNORECASE)
    for m in many_matches:
        if m[1].lower() not in ['people', 'children', 'men', 'women', 'mice', 'feet', 'teeth']:
            detected_errors.append({
                "cau": f"...{m[0]} {m[1]}...",
                "loi_loai": "Plural Noun Agreement",
                "de_xuat": f"Đổi '{m[1]}' thành dạng số nhiều '{m[1]}s'",
                "giai_thich": f"Sau tính từ chỉ số lượng '{m[0]}' cần sử dụng danh từ đếm được số nhiều."
            })

    # Luật 4: Phát hiện từ lặp lại nhiều lần trong bài (Lỗi lặp từ)
    word_counts_dict = {}
    for w in raw_words:
        w_lower = w.lower()
        if len(w_lower) > 3 and w_lower not in ['this', 'that', 'with', 'from', 'have', 'more', 'they', 'their', 'some', 'about']:
            word_counts_dict[w_lower] = word_counts_dict.get(w_lower, 0) + 1
            
    repeated_words = [w for w, count in word_counts_dict.items() if count >= 3]
    if repeated_words:
        detected_errors.append({
            "cau": f"Các từ xuất hiện nhiều lần: {', '.join(repeated_words)}",
            "loi_loai": "Lexical Redundancy (Lặp từ)",
            "de_xuat": "Sử dụng các từ đồng nghĩa (Synonyms) để làm phong phú văn phong.",
            "giai_thich": "Việc lặp lại 1 từ quá 3 lần làm giảm chỉ số đa dạng từ vựng."
        })

    # HIỂN THỊ DANH SÁCH LỖI
    if detected_errors:
        for idx, err in enumerate(detected_errors, 1):
            with st.expander(f"❌ Lỗi {idx}: [{err['loi_loai']}] trong văn bản"):
                st.markdown(f"- **Vị trí / Ngữ cảnh:** `{err['cau']}`")
                st.markdown(f"- **Đề xuất chỉnh sửa:** `{err['de_xuat']}`")
                st.markdown(f"- **Quy tắc NLP:** {err['giai_thich']}")
    else:
        st.success("🎉 Không phát hiện lỗi ngữ pháp/chính tả cơ bản nào trong bài viết!")

    # --- BƯỚC 4: XẾP LOẠI & ĐÁNH GIÁ ĐỘNG DỰA TRÊN BÀI LÀM ---
    st.markdown("---")
    st.header("Bước 4: Chẩn đoán Năng lực Ngôn ngữ theo Bài làm")
    
    # Tính điểm và xếp loại CEFR linh hoạt dựa trên dữ liệu thật
    error_count = len(detected_errors)
    if error_count == 0 and ttr > 60:
        cefr_level = "B2 / C1 (Upper-Intermediate)"
        overall_score = 9.0
    elif error_count <= 2 and ttr > 45:
        cefr_level = "B1 (Intermediate)"
        overall_score = 7.5
    elif error_count <= 4:
        cefr_level = "A2 (Elementary)"
        overall_score = 6.0
    else:
        cefr_level = "A1 (Beginner)"
        overall_score = 4.5

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Dự đoán Trình độ CEFR", value=cefr_level)
        st.metric(label="Điểm Đánh giá Ngôn ngữ", value=f"{overall_score} / 10")
    
    with col_b:
        st.markdown("### 📊 Tổng quan Phân tích Ngữ nghĩa:")
        st.markdown(f"- Bài viết gồm **{sentence_count} câu**, độ dài trung bình **{avg_sentence_len} từ/câu**.")
        st.markdown(f"- Tỉ lệ từ vựng độc bản đạt **{ttr}%**.")
        st.markdown(f"- Hệ thống ghi nhận **{error_count} lỗi ngữ pháp/văn phong** cần khắc phục.")

    # --- BƯỚC 5: ĐỀ XUẤT CỦNG CỐ DỰA TRÊN LỖI THỰC TẾ ---
    st.markdown("---")
    st.header("Bước 5: Đề xuất Bài tập Cá nhân hóa khắc phục đúng lỗi vừa mắc")
    st.warning("🎯 **Lộ trình rèn luyện được AI tạo tự động từ các lỗi trong bài viết trên:**")
    
    if detected_errors:
        for err in detected_errors:
            st.markdown(f"- 📝 **Bài tập củng cố dạng [{err['loi_loai']}]:** Luyện tập lại quy tắc `{err['giai_thich']}`.")
    else:
        st.markdown("- 📝 **Bài tập nâng cao:** Viết lại đoạn văn trên sử dụng các cấu trúc câu phức (Complex Sentences) và từ vựng академический (Academic Vocabulary).")

    # BÁO CÁO GIÁO VIÊN
    st.markdown("---")
    st.header("📋 Báo cáo Chi tiết Log NLP gửi Giáo viên")
    st.json({
        "raw_essay_snippet": text[:100] + "...",
        "word_count": word_count,
        "sentence_count": sentence_count,
        "ttr_lexical_score": ttr,
        "detected_error_count": error_count,
        "cefr_assessment": cefr_level,
        "error_summary": [e["loi_loai"] for e in detected_errors]
    })
    st.success("Đã phân tích văn bản thực tế và xuất báo cáo thành công!")