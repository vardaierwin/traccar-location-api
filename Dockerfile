FROM traccar/traccar:6.5

# Copy configuration file
COPY traccar.xml /opt/traccar/conf/traccar.xml

# Expose the web port
EXPOSE 8082

# Run Traccar
CMD ["java", "-Xms1g", "-Xmx1g", "-Djava.net.preferIPv4Stack=true", "-jar", "/opt/traccar/tracker-server.jar", "/opt/traccar/conf/traccar.xml"]