"""
التصورات البيانية باستخدام Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config.settings import CHART_COLORS
from utils.logger import app_logger
import arabic_reshaper
from bidi.algorithm import get_display


class SentimentVisualizer:
    """فئة لإنشاء الرسوم البيانية"""

    def __init__(self):
        """تهيئة الرسام"""
        self.colors = CHART_COLORS

    def _fix_arabic_text(self, text):
        """
        إصلاح عرض النص العربي

        Args:
            text: النص العربي

        Returns:
            str: النص المعدل
        """
        if not isinstance(text, str):
            return str(text)

        try:
            reshaped = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped)
            return bidi_text
        except:
            return text

    def plot_sentiment_pie(self, sentiment_counts, title="توزيع المشاعر"):
        """
        رسم دائري لتوزيع المشاعر

        Args:
            sentiment_counts: dict أو Series بعدد كل فئة
            title: عنوان الرسم

        Returns:
            plotly.graph_objects.Figure
        """
        if isinstance(sentiment_counts, dict):
            labels = list(sentiment_counts.keys())
            values = list(sentiment_counts.values())
        elif isinstance(sentiment_counts, pd.Series):
            labels = sentiment_counts.index.tolist()
            values = sentiment_counts.values.tolist()
        else:
            app_logger.error("نوع البيانات غير صحيح لـ sentiment_counts")
            return go.Figure()

        # إصلاح النصوص العربية
        labels_display = [self._fix_arabic_text(label) for label in labels]
        title_display = self._fix_arabic_text(title)

        # تحديد الألوان
        colors_map = {
            'إيجابي': self.colors['positive'],
            'سلبي': self.colors['negative'],
            'محايد': self.colors['neutral']
        }
        colors_list = [colors_map.get(label, '#999999') for label in labels]

        fig = go.Figure(data=[go.Pie(
            labels=labels_display,
            values=values,
            hole=0.3,
            marker=dict(colors=colors_list, line=dict(color='white', width=2)),
            textinfo='label+percent',
            textfont=dict(size=14, family='Arial'),
            hovertemplate='<b>%{label}</b><br>العدد: %{value}<br>النسبة: %{percent}<extra></extra>'
        )])

        fig.update_layout(
            title=dict(
                text=title_display,
                font=dict(size=20, family='Arial'),
                x=0.5,
                xanchor='center'
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            height=500,
            margin=dict(t=80, b=100)
        )

        return fig

    def plot_word_frequency_bar(self, word_freq_df, title="الكلمات الأكثر تكراراً", top_n=15):
        """
        رسم عمودي للكلمات الأكثر تكراراً

        Args:
            word_freq_df: DataFrame بعمودين (word, frequency)
            title: عنوان الرسم
            top_n: عدد الكلمات المعروضة

        Returns:
            plotly.graph_objects.Figure
        """
        if word_freq_df.empty:
            return go.Figure()

        # أخذ أول top_n كلمة
        df = word_freq_df.head(top_n).copy()

        # إصلاح النصوص العربية
        df['word_display'] = df['word'].apply(self._fix_arabic_text)
        title_display = self._fix_arabic_text(title)

        # ترتيب تصاعدي للعرض (الأكثر في الأعلى)
        df = df.sort_values('frequency', ascending=True)

        fig = go.Figure(data=[go.Bar(
            x=df['frequency'],
            y=df['word_display'],
            orientation='h',
            marker=dict(
                color=df['frequency'],
                colorscale='Blues',
                showscale=False,
                line=dict(color='white', width=1)
            ),
            text=df['frequency'],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>التكرار: %{x}<extra></extra>'
        )])

        fig.update_layout(
            title=dict(
                text=title_display,
                font=dict(size=20, family='Arial'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title=self._fix_arabic_text('التكرار'),
                showgrid=True,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='',
                tickfont=dict(size=12, family='Arial')
            ),
            height=max(400, top_n * 30),
            margin=dict(l=150, r=50, t=80, b=50),
            plot_bgcolor='white'
        )

        return fig

    def plot_sentiment_timeline(self, time_sentiment_df, title="تطور المشاعر عبر الزمن"):
        """
        رسم خطي لتطور المشاعر عبر الوقت

        Args:
            time_sentiment_df: DataFrame مع فهرس زمني وأعمدة المشاعر
            title: عنوان الرسم

        Returns:
            plotly.graph_objects.Figure
        """
        if time_sentiment_df.empty:
            return go.Figure()

        title_display = self._fix_arabic_text(title)

        fig = go.Figure()

        # إضافة خط لكل فئة مشاعر
        sentiment_colors = {
            'إيجابي': self.colors['positive'],
            'سلبي': self.colors['negative'],
            'محايد': self.colors['neutral']
        }

        for col in time_sentiment_df.columns:
            color = sentiment_colors.get(col, '#999999')
            col_display = self._fix_arabic_text(col)

            fig.add_trace(go.Scatter(
                x=time_sentiment_df.index,
                y=time_sentiment_df[col],
                mode='lines+markers',
                name=col_display,
                line=dict(color=color, width=3),
                marker=dict(size=6),
                hovertemplate='<b>%{fullData.name}</b><br>الوقت: %{x}<br>النسبة: %{y:.1f}%<extra></extra>'
            ))

        fig.update_layout(
            title=dict(
                text=title_display,
                font=dict(size=20, family='Arial'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title=self._fix_arabic_text('الوقت'),
                showgrid=True,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title=self._fix_arabic_text('النسبة (%)'),
                showgrid=True,
                gridcolor='lightgray',
                range=[0, 100]
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            ),
            height=500,
            plot_bgcolor='white',
            hovermode='x unified'
        )

        return fig

    def plot_engagement_sentiment(self, df, title="التفاعل مقابل المشاعر"):
        """
        رسم نقطي يربط بين التفاعل والمشاعر

        Args:
            df: DataFrame يحتوي على likes, retweets, sentiment
            title: عنوان الرسم

        Returns:
            plotly.graph_objects.Figure
        """
        if df.empty:
            return go.Figure()

        required_cols = ['likes', 'retweets', 'sentiment']
        if not all(col in df.columns for col in required_cols):
            app_logger.warning("الأعمدة المطلوبة غير موجودة")
            return go.Figure()

        title_display = self._fix_arabic_text(title)

        # حساب التفاعل الكلي
        df_plot = df.copy()
        df_plot['total_engagement'] = df_plot['likes'] + df_plot['retweets']

        # تصفية القيم الصفرية أو السالبة للـ log scale
        df_plot = df_plot[df_plot['total_engagement'] > 0]

        if df_plot.empty:
            return go.Figure()

        # تعيين الألوان
        sentiment_colors = {
            'إيجابي': self.colors['positive'],
            'سلبي': self.colors['negative'],
            'محايد': self.colors['neutral']
        }

        fig = go.Figure()

        for sentiment in df_plot['sentiment'].unique():
            df_sentiment = df_plot[df_plot['sentiment'] == sentiment]
            sentiment_display = self._fix_arabic_text(sentiment)

            fig.add_trace(go.Scatter(
                x=df_sentiment['likes'],
                y=df_sentiment['retweets'],
                mode='markers',
                name=sentiment_display,
                marker=dict(
                    size=8,
                    color=sentiment_colors.get(sentiment, '#999999'),
                    opacity=0.6,
                    line=dict(width=1, color='white')
                ),
                hovertemplate='<b>%{fullData.name}</b><br>الإعجابات: %{x}<br>إعادة التغريد: %{y}<extra></extra>'
            ))

        fig.update_layout(
            title=dict(
                text=title_display,
                font=dict(size=20, family='Arial'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title=self._fix_arabic_text('عدد الإعجابات'),
                type='log',
                showgrid=True,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title=self._fix_arabic_text('عدد إعادات التغريد'),
                type='log',
                showgrid=True,
                gridcolor='lightgray'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            ),
            height=500,
            plot_bgcolor='white',
            hovermode='closest'
        )

        return fig

    def create_stats_cards(self, stats):
        """
        إنشاء بطاقات إحصائية (للاستخدام مع Streamlit metrics)

        Args:
            stats: dict الإحصائيات

        Returns:
            dict: البيانات المنسقة للعرض
        """
        return {
            'positive': {
                'value': stats.get('positive', 0),
                'percentage': stats.get('positive_pct', 0),
                'color': self.colors['positive']
            },
            'negative': {
                'value': stats.get('negative', 0),
                'percentage': stats.get('negative_pct', 0),
                'color': self.colors['negative']
            },
            'neutral': {
                'value': stats.get('neutral', 0),
                'percentage': stats.get('neutral_pct', 0),
                'color': self.colors['neutral']
            }
        }


# دوال مساعدة للاستخدام السريع
def quick_pie_chart(sentiment_counts):
    """
    إنشاء رسم دائري سريع

    Args:
        sentiment_counts: عدد كل فئة

    Returns:
        Figure: الرسم
    """
    viz = SentimentVisualizer()
    return viz.plot_sentiment_pie(sentiment_counts)


def quick_bar_chart(word_freq_df, top_n=15):
    """
    إنشاء رسم عمودي سريع

    Args:
        word_freq_df: DataFrame الكلمات
        top_n: عدد الكلمات

    Returns:
        Figure: الرسم
    """
    viz = SentimentVisualizer()
    return viz.plot_word_frequency_bar(word_freq_df, top_n=top_n)
