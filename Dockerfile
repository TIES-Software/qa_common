# default image if none is provided in Jenkins
ARG IMAGE="tiesqa/chrome_current:chrome_current_python3"

FROM $IMAGE

ARG BUILD_TYPE="current"

ENV BUILD_TYPE=$BUILD_TYPE
ENV CHROME_DRIVER="/usr/local/bin/chromedriver"
ENV OLD_CHROMEDRIVER_DIR_LINUX="/usr/local/bin/"
ENV CHROME_DRIVER_DIR="/usr/local/bin/chromedriver"
ENV FIREFOX_BINARY_PATH="/usr/bin"
ENV GECKO_DRIVER="/usr/bin"
ENV FP_QA_EMAIL_ACCT="ci@feepay.com"
ENV DISPLAY=:99
ENV PROD_ID="test"
ENV ROSTER_USER="ci+rosterview@feepay.com"
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin/chromedriver:/etc/source"
ENV OLD_CHROMEDRIVER_DIR="/usr/local/bin/chromedriver"
ENV FEEPAY_PASS=""
ENV FP_QA_EMAIL_PASS=""
ENV FP_LEGACYPUSH_TOKEN=""
ENV ROSTER_PASS=""
ENV PROD_PASS=""
ENV CHROME_OLD_BROWSER="/usr/bin/chromium-browser"
ENV PWD="/etc/source/ui_tests/feepay_euronymo"
ENV PYTHONPATH="/etc/source"
COPY . /etc/source
WORKDIR /etc/source

RUN echo "------------------------------------------" \
    # default ubuntu image does not have this
    && apt-get install libssl1.0.0 \
    && echo "Creating ODBC files" \
    && echo "------------------------------------------" \
    && echo "[MySQLServerDatabase] \nDriver      = /opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.2.so.0.1 \nDescription = My MS SQL Server \nTrace = No \nServer = 192.168.100.46 \nDatabase = FeePay.IntegrationsData" >> /etc/odbc.ini \
    && echo "[MySQLServerDatabase] \nDescription = ODBC 3.51.30 for MySQL \nDriver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.2.so.0.1\n Setup=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.2.so.0.1 \nUsageCount=1" >> /etc/odbcinst.ini

CMD ["bash"]
