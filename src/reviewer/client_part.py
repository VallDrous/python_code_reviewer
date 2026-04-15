import streamlit as st
from reviewer import server_part as sp

if "files_code" not in st.session_state:
    st.session_state.files_code = ''
    
if "result" not in st.session_state:
    st.session_state.result = {
        "result": "",
        "is_error": False
    } 

key = st.text_input('Введіть коректний ключ для роботи з системою')

error_placeholder = st.empty()

uploaded_files = st.file_uploader(
    "Завантаж Python файли",
    type=["py"],
    accept_multiple_files=True
)

if uploaded_files:
    st.session_state.files_code = ''
    for file in uploaded_files:
        code = file.read().decode("utf-8")
        
        st.write(f"Файл: {file.name}")
        st.code(code, language="python")
        st.session_state.files_code += f"{file.name}\n{code}\n\n" 
        
col1, col2, col3 = st.columns([1,1,1])     
   
with col2:  
    if st.button('Провести аналіз коду'):
        error_placeholder.empty()
        st.session_state.result = {
            "result": "",
            "is_error": False
        }
        if key.strip() != '' and st.session_state.files_code.strip() != '': 
            st.session_state.result = sp.analize_code(key, st.session_state.files_code)  
        elif not key.strip():
            error_placeholder.error("Поле ключа не може бути порожнім!")  
        elif not st.session_state.files_code.strip():
            st.warning("Завантажте файли для аналізу")

if not st.session_state.result['is_error'] and st.session_state.result['result'] != "":
    res = st.session_state.result['result']
    st.metric(label="Складність та показник якості", value=f"{res.complexity_score} / 10")            
    tab1, tab2, tab3 = st.tabs(["PEP 8", "Безпека", "Рефакторинг"])

    with tab1:
        if res.pep8_violations:
            for issue in res.pep8_violations:
                st.write(f"- {issue}")
        else:
            st.success("Порушень PEP 8 не виявлено!")

    with tab2:
        if res.vulnerabilities:
            for vuln in res.vulnerabilities:
                st.error(f"Знайдено: {vuln}")
        else:
            st.success("Критичних вразливостей не знайдено.")

    with tab3:
        st.markdown(res.refactoring_suggestions)
elif st.session_state.result['is_error']:
    st.error(st.session_state.result['result'])