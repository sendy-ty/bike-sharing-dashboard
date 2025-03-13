import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# ========================== #
# 🔹 Konfigurasi Dashboard 🔹 #
# ========================== #
st.set_page_config(
    page_title="Bike Sharing & Customer Segmentation Dashboard",
    page_icon="🚲",
    layout="wide"
)

# ========================== #
# 🔹 Membaca Dataset dengan Fallback Strategy 🔹 #
# ========================== #

# Path file
possible_data_paths = [
    Path(os.path.dirname(os.path.abspath(__file__))) / "data.csv",
    Path(os.getcwd()) / "data.csv",
    Path(os.getcwd()) / "dashboard" / "data.csv",
    Path(os.getcwd()).parent / "data.csv",
    Path("/mount/src/submission-analisisdata/dashboard/data.csv"),
    Path("/mount/src/submission-analisisdata/data.csv")
]

possible_rfm_paths = [
    Path(os.path.dirname(os.path.abspath(__file__))) / "customer_segmentation.csv",
    Path(os.getcwd()) / "customer_segmentation.csv",
    Path(os.getcwd()) / "dashboard" / "customer_segmentation.csv",
    Path(os.getcwd()).parent / "customer_segmentation.csv",
    Path("/mount/src/submission-analisisdata/dashboard/customer_segmentation.csv"),
    Path("/mount/src/submission-analisisdata/customer_segmentation.csv")
]

# Logging lokasi file untuk debugging
with st.expander("📂 Debug Info (File Paths)"):
    st.write("Current working directory:", os.getcwd())
    st.write("Script directory:", os.path.dirname(os.path.abspath(__file__)))
    st.write("Possible data paths:")
    for path in possible_data_paths:
        st.write(f"- {path} (exists: {path.exists()})")
    st.write("Possible RFM paths:")
    for path in possible_rfm_paths:
        st.write(f"- {path} (exists: {path.exists()})")

# Fungsi untuk mencari file yang ada
def find_existing_file(possible_paths):
    for path in possible_paths:
        if path.exists():
            return str(path)
    return None

# Cari file data
data_file = find_existing_file(possible_data_paths)
rfm_file = find_existing_file(possible_rfm_paths)

# Membaca data
df = None
if data_file:
    try:
        df = pd.read_csv(data_file)
        st.success(f"✅ Dataset berhasil dimuat dari: {data_file}")
    except Exception as e:
        st.error(f"❌ Error saat membaca file data: {e}")
else:
    st.warning("⚠️ File data.csv tidak ditemukan. Silakan upload file:")
    uploaded_data = st.file_uploader("Upload file data.csv", type="csv")
    if uploaded_data:
        try:
            df = pd.read_csv(uploaded_data)
            st.success("✅ Dataset berhasil dimuat dari uploaded file!")
        except Exception as e:
            st.error(f"❌ Error saat membaca uploaded file: {e}")

df_rfm = None
if rfm_file:
    try:
        df_rfm = pd.read_csv(rfm_file)
        st.success(f"✅ Dataset RFM berhasil dimuat dari: {rfm_file}")
    except Exception as e:
        st.error(f"❌ Error saat membaca file RFM: {e}")
else:
    st.warning("⚠️ File customer_segmentation.csv tidak ditemukan. Silakan upload file:")
    uploaded_rfm = st.file_uploader("Upload file customer_segmentation.csv", type="csv")
    if uploaded_rfm:
        try:
            df_rfm = pd.read_csv(uploaded_rfm)
            st.success("✅ Dataset RFM berhasil dimuat dari uploaded file!")
        except Exception as e:
            st.error(f"❌ Error saat membaca uploaded file: {e}")
if df is None or df_rfm is None:
    st.error("❌ Data tidak lengkap. Dashboard tidak dapat ditampilkan.")
    st.stop()

# ========================== #
# 🔹 Header Dashboard 🔹 #
# ========================== #
st.markdown("<h1 style='text-align: center;'>🚲 Bike Sharing & Customer Segmentation 📊</h1>", unsafe_allow_html=True)

# ========================== #
# 🔹 Filter Data 🔹 #
# ========================== #
st.sidebar.header("🔎 Filter Data")
segment_options = df_rfm['Customer_Segment'].unique().tolist()
selected_segment = st.sidebar.multiselect("Pilih Segmentasi Customer", segment_options, default=segment_options)

# ========================== #
# 🔹 Tabel Segmentasi Customer 🔹 #
# ========================== #
st.subheader("📋 Tabel Segmentasi Customer")
filtered_df = df_rfm[df_rfm['Customer_Segment'].isin(selected_segment)]
st.dataframe(filtered_df.head(10))  

# ========================== #
# 🔹 Visualisasi Distribusi Customer 🔹 #
# ========================== #
st.subheader("👥 Distribusi Customer Berdasarkan Segmentasi RFM")

# Mengecek apakah kolom 'Customer_Segment' tersedia
df_rfm['Customer_Segment'] = df_rfm['Customer_Segment'].astype(str)  
customer_count = df_rfm['Customer_Segment'].value_counts().reset_index()
customer_count.columns = ["Segment", "Jumlah Customer"]
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=customer_count, x="Segment", y="Jumlah Customer", palette="pastel", ax=ax)
ax.set_xlabel("Kategori Customer")
ax.set_ylabel("Jumlah Customer")
ax.set_title("Distribusi Customer Berdasarkan Segmentasi RFM")
plt.xticks(rotation=30)
st.pyplot(fig)

# ========================== #
# 🔹 Statistik Ringkasan 🔹 #
# ========================== #
st.sidebar.subheader("📊 Statistik Ringkasan")
if "Customer_ID" in df_rfm.columns:
    total_customer = df_rfm.groupby("Customer_Segment")["Customer_ID"].count().reset_index()
    total_customer.columns = ["Segment", "Total Customer"]
    st.sidebar.write("Total Customer per Segmentasi:")
    st.sidebar.dataframe(total_customer)

# ========================== #
# 🔹 Footer Dashboard 🔹 #
# ========================== #
st.markdown("---")
st.markdown("<p style='text-align: center;'> Sandy Tirta Yudha | © 2025</p>", unsafe_allow_html=True)