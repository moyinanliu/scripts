# 使用方法： salt '*' state.sls file_sync pillar="{'src':'salt://test.txt', 'dst':'/tmp/test.txt'}"
file_sync_1:
  file.managed:
    - name: {{ pillar['dst'] }}
    - source: {{ pillar['src'] }}
    
