file_sync_1:
  file.managed:
    - name: {{ pillar['dst'] }}
    - source: {{ pillar['src'] }}
    
