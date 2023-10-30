# 메인화면 라우터
@app.route("/", methods=["GET", "POST"])
def m_settings(): # 값을 변경한 경우, 업데이트해주는 함수 
    global pill_amount, target_hour, target_minute
    
    if request.method == "POST":
        # POST 요청을 처리하여 설정을 업데이트
        pill_amount = int(request.form.get("pill_amount"))
        target_hour = int(request.form.get("target_hour"))
        target_minute = int(request.form.get("target_minute"))
        
        # 설정이 업데이트된 후에 다시 settings.html을 리턴
        return render_template("settings.html", pill_amount=pill_amount, target_hour=target_hour, target_minute=target_minute)
    return render_template("settings.html", pill_amount=pill_amount, target_hour=target_hour, target_minute=target_minute)

def check_pill_time(): # 복용 시간 체크 함수
    global pill_amount, target_hour, target_minute
    while True: 
        # 현재 시, 분 저장
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min

        if current_hour == target_hour and current_minute == target_minute: 
				# 현재 시간이 복용 시간과 같을 경우 pro 함수 실행
            pro() 

        time.sleep(10)  # 10초마다 확인
