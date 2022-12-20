
python download.py && \
python process_downloaded.py
cd reports
jupyter nbconvert --to notebook --execute PostStatistics.ipynb
mv PostStatistics.nbconvert.ipynb PostStatistics.ipynb
