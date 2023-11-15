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




@app.route("/pillstart")
# 현재 시간과 복용 시간이 같은 경우에 실행되는 함수
def pro():
    global pill_amount, target_hour, target_minute, pill
    try:
        while True:
            # 현재 시간 가져오기
            current_time = time.localtime()
            current_hour = current_time.tm_hour
            current_minute = current_time.tm_min
            # 화면 초기화
            draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
            # 복용시간 + 복용여부 출력
            draw.text((0,10), str(target_hour)+" : "+str(target_minute)+"    "+str(pill), font=font, fill=255)
            # 현재시간 출력
            draw.text((0,30), str(current_hour)+" : "+str(current_minute), font=font, fill=255)
            oled.image(image)
            oled.show()
            # 설정한 시간에 LED , 부저 켜기
            if pill == False and current_hour == target_hour and current_minute == target_minute:
                GPIO.output(led, 1)
                p.ChangeFrequency(100)
                p.start(50)
                print("LED 켜짐")
                GPIO.input(hc) # 적외선 센서 켜서 사람 감지
								
								# 사람이 감지된 경우
                if GPIO.input(hc) == 1:
										# 서보모터 켜서 입구 열기
										ser.start(0)
                    time.sleep(3)
                    ser.ChangeDutyCycle(7.5)
                    time.sleep(3)
                    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
                    draw.text((0,10), str("Take your medication"), font=font2, fill=255)
                    draw.text((0,30), str(current_hour)+" : "+str(current_minute), font=font, fill=255)
                    oled.image(image)
                    oled.show()
                    GPIO.output(led, 0)
                    p.stop()
										# 사람 감지되었으므로 led, 부저 끄기
										# 입구 닫기
                    ser.ChangeDutyCycle(2.5)
                    time.sleep(3)
										# 알약 복용 여부 True
                    pill = True

            # 알약 복용 확인된 경우
            if pill == True:
                pill_amount -= 1 # 남은 약 -1
                pill_data[f'{current_month:02d}-{current_day:02d}'] = "O" 
								# 복용여부 변경
                draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
                # 복용시간 + 변경된 복용여부 oled 출력
                draw.text((0,10), str(target_hour)+" : "+str(target_minute)+"    "+str(pill), font=font, fill=255)
                # 현재시간 oled 출력
                draw.text((0,30), str(current_hour)+" : "+str(current_minute), font=font, fill=255)
                oled.image(image)
                oled.show()
                return pillaa(pill_data=pill_data, pill_amount=pill_amount, target_hour=target_hour, target_minute=target_minute)
                # pillaa 함수로 리턴
    
		# 예외처리
    except KeyboardInterrupt:
        print("stopped by user")
        GPIO.cleanup()
        return render_template('index.html', pill_data=pill_data, pill_amount=pill_amount, target_hour=target_hour, target_minute=target_minute)


@app.route("/pilla")
# pro에서 호출됨
def pillaa(pill,pill_data, pill_amount, target_hour, target_minute):
    if pill == True: # 복용여부 O일 경우
        pill_data_temp[3][pill_data] = "O" 
				# 변경된 데이터를 일주일 데이터에 넣어주기
        page = request.args.get('page', type=int, default=3)
        page_temp = pill_data_temp[page] 
				# 일주일씩 데이터 출력
    return render_template('index.html', pill_data=page_temp, pill_amount=pill_amount, target_hour=target_hour, target_minute=target_minute, page=page)
