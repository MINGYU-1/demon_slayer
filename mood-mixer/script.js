const energySlider = document.getElementById('energy-slider');
const body = document.body;

// 에너지 레벨에 따라 배경색 변경
energySlider.addEventListener('input', (event) => {
    const value = event.target.value;
    // value(1~100)를 HSL 색상값으로 변환 (240(파랑) ~ 0(빨강))
    const hue = 240 - (value * 2.4);
    body.style.backgroundColor = `hsl(${hue}, 50%, 20%)`;
});

// 키워드 버튼 활성화/비활성화
const keywordBtns = document.querySelectorAll('.keyword-btn');
keywordBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        btn.classList.toggle('active');
    });
});

// 최종 버튼 클릭 이벤트 (실제로는 여기서 DB와 연동하여 결과를 보여줌)
const findTrackBtn = document.getElementById('find-track-btn');
findTrackBtn.addEventListener('click', () => {
    const energy = energySlider.value;
    const vibe = document.getElementById('vibe-slider').value;
    const activeKeywords = document.querySelectorAll('.keyword-btn.active');
    const selectedKeywords = Array.from(activeKeywords).map(btn => btn.textContent);

    console.log('Energy:', energy, 'Vibe:', vibe, 'Keywords:', selectedKeywords);
    alert('믹싱 완료! 당신의 트랙을 찾는 중...');
    // 여기에 결과 카드 UI를 생성하고 보여주는 로직을 추가합니다.
});