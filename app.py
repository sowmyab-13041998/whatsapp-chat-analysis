import streamlit as st
import preprocessing, helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsup chat analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessing.preprocess(data)


    # To fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # Adding button
    if st.sidebar.button("Show analysis"):
        num_message, words, num_media_message, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        c1, c2, c3, c4 = st.columns(4) # c is the columns

        with c1:
            st.header("Total messages")
            st.title(num_message)
        with c2:
            st.header("Total words")
            st.title(words)
        with c3:
            st.header("Total media shared")
            st.title(num_media_message)
        with c4:
            st.header("Total links shared")
            st.title(num_links)

        # montly Timeline

        st.title("Montly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # week activity timeline
        st.title("Weekly activity map")

        c1, c2 = st.columns(2)

        with c1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='magenta')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with c2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # weekly activity map

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # Finding the busiest users in the group

        if selected_user == 'Overall':
            st.title("Most busy users")
            x,new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            c1, c2 = st.columns(2)

            with c1:
                ax.bar(x.index, x.values, color='cyan')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with c2:
                st.dataframe(new_df)

        # wordCloud
        st.title("WorldCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)
        st.set_option('deprecation.showPyplotGlobalUse', False)

        # Most commom words

        most_common_df = helper.most_commom_words(selected_user,df)
        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1], color='lime')
        plt.xticks(rotation='vertical',)

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        c1,c2 = st.columns(2)

        with c1:
            st.dataframe(emoji_df)
        with c2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)










