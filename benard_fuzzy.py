try:
    import streamlit as st
    from PIL import Image
    image = Image.open('FuzzyLookup.png')
    st.sidebar.image(image,use_column_width=True)
    st.sidebar.write("""Fuzzy lookup App""")
    st.sidebar.write("""***By: Smallpdf Kenya*** """)
    link1 = '[Fuzzy Lookup](https://fuzzylookup.com/)'
    st.sidebar.markdown(link1, unsafe_allow_html=True)


    import pandas as pd
    import numpy as np
    import fuzzy_pandas as fpd
    from string_grouper import match_strings, match_most_similar, \
    group_similar_strings, compute_pairwise_similarities, \
    StringGrouper
    import warnings
    warnings.filterwarnings('ignore')
    st.write("""# Fuzzy lookup data tool. Join data based on text similarity.""")
    st.write("""***Just drag and drop your file.***""")

    uploaded_file1 = st.file_uploader("Choose first dataset", type=['csv', 'xlsx'])
    uploaded_file2 = st.file_uploader("Choose second dataset", type=['csv', 'xlsx'])
    if uploaded_file1 is not None:
        try:
            df1 = pd.read_csv(uploaded_file1)
        except Exception as e:
            df1 = pd.read_excel(uploaded_file1)

        if uploaded_file2 is not None:
            try:
                df2 = pd.read_csv(uploaded_file2)
            except Exception as e:
                df2 = pd.read_excel(uploaded_file2)
            
            st.write("""***First dataset***""")
            st.dataframe(df1)
            st.write("""***Second dataset***""")
            st.dataframe(df2)

            left_col = st.selectbox('Select column to be matched from first dataset', df1.columns)
            right_col = st.selectbox('Select column to be matched from second dataset', df2.columns)
            method_list = ['exact','levenshtein','jaro','metaphone','bilenko']
            methods = st.selectbox('Select method',method_list)
            join_list = ['inner', 'left-outer', 'right-outer', 'full-outer']
            join = st.selectbox('Join method',join_list)
            
            st.write('Select a threshold value:')
            t = st.slider("Minimum Similarity (%)", min_value=0.0, max_value=1.0,value=0.6,step=0.05)

            show_result = st.radio("Result columns",('Only selected columns', 'All columns'))
            
            if show_result == 'Only selected columns':
                matches = fpd.fuzzy_merge(df1, df2,
                                    left_on=left_col,
                                    right_on=right_col,
                                    ignore_case=True,
                                    threshold=t,
                                    keep='match',
                                    method=methods,
                                    join=join)

            if show_result == 'All columns':
                matches = fpd.fuzzy_merge(df1, df2,
                                    left_on=left_col,
                                    right_on=right_col,
                                    ignore_case=True,
                                    threshold=t,
                                    method=methods,
                                    join=join)


            if(st.button('Run')):
                
                st.write("""***Results***""")
                st.write('Number of matches are',len(matches.index))
                st.dataframe(matches)

                import base64
                from io import BytesIO
                def filedownload(df):              # Function Code snippet for downloading as .csv file (Source: https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806 )
                    csv = df.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
                    href = f'<a href="data:file/csv;base64,{b64}" download="result.csv">Download .csv file</a>'
                    return href
                st.markdown(filedownload(matches), unsafe_allow_html=True)

                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    df.to_excel(writer, sheet_name='Sheet1')
                    writer.save()
                    processed_data = output.getvalue()
                    return processed_data

                def get_table_download_link(df):
                    """Generates a link allowing the data in a given panda dataframe to be downloaded
                    in:  dataframe
                    out: href string
                    """
                    val = to_excel(df)
                    b64 = base64.b64encode(val)  # val looks like b'...'
                    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="result.xlsx">Download .xlsx file</a>' # decode b'abc' => abc

                
                st.markdown(get_table_download_link(matches), unsafe_allow_html=True)

                st.success('Done!')

except:
    pass

    

    
