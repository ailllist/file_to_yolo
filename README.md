# file_to_yolo

> .json 파일을 yolov5의 형식에 맞추어 변환해줍니다.    
> 일반적으로 모든 .json파일에 대응되는 코드가 아니기 때문에, 코드의 구조만 참고해주면 됩니다.
>> ### 코드 구조 설명
>>+ json converting
>>+ validation dataset maker    
> ### json converting
> json 파일을 yolov5의 txt파일로 바꾸는 부분입니다. code order 파일에서 확인할 수 있듯 다음과 같은 절차로 구성되어있습니다.
>+ (multi) image checker
>+ lbl_matcher
>+ convertor
>+ remover
> ### Image checker
> 이미지의 크기가 지정한 크기와 맞지 않을 경우 이미지를 삭제해주는 코드입니다.    
> 주로 여러가지 이미지 크기 (ex. 1920 * 1080, 1920 * 1200, 1280 * 720...)에서 특정 크기를 가진 이미지만을 제외하고는 전부 삭제합니다.
> 이 경우 converting의 첫번째 부분이기에 processing 과정중 제일 많은 데이터를 처리하기 때문에. multi processing을 사용해 병렬처리를 구현한 코드
> multi_img_checker를 사용해 이미지를 삭제할 수 있습니다.
> ### lbl_matcher
> image checker의 실행결과 삭제된 이미지에 대응되는 라벨을 지워줍니다.    
> 작동 원리가 이미지 이름에 대응되는 라벨링 파일이 없다면 삭제하는 구조이기 때문에 이미지와 라벨의 수가 맞기 않을 때 필터링에 사용할 수 있습니다.
> ### converter
> json파일을 yolov5의 형식에 맞추어 변환해주는 코드입니다.    
> json파일의 대상데이터에 따라 코드의 핵심부분을 변경해줘야한다는 번거로움이 있습니다.
> 예시 코드는 신호등을 분류하는 코드입니다.    
> 본 코드의 핵심은 json파일 전체를 eval() 함수를 사용해 python dictionary자료형으로서 json파일을 처리한다는 점입니다. 만약 json파일이 일련의 이유로
> eval()키워드가 적용이 되지 않는 경우 새로이 변환 코드를 구성해주어야 합니다.
> 보통 한번 dictionay로 변환이 된 경우 json파일에서처럼 순차적으로 dictionary로 접근이 가능합니다.    
> 
> json 파일의 구조를 잘 분석하여 적절히 코드를 변형해 사용해주세요.    
>+ EXTEND_FACTOR   
> bounding box의 크기를 확장해줄때 사용합니다. 만약 본인이 사용하는 데이터의 라벨링 박스 크기가 작다고 생각이 들면 해당 변수를 수정해주세요.
> width (pixel) * EXTEND_FACTOR, height (pixel) * EXTEND_FACTOR 입니다.
>+ MINIMUM_BOX_SIZE    
> 해당 크기보다 작은 면적을 가진 bounding box를 무시합니다.
>+ MAX_CLASS_NuMBER    
> Class_num을 잘못구했을때를 대비하여 선언한 변수입니다. 만약 최종 class_num이 해당 변수보다 크다면, 해당 bounding box를 무시합니다.
> ### remover
> converting되지 못한 라벨에 대응되는 이미지를 삭제합니다. 
> 
> # Additional
> ### error_remover.py
> 주어진 class_num 보다 큰 숫자를 가진 라벨링 파일이 있으면 해당 파일을 삭제하고, 해당 파일에 대응되는 이미지도 삭제하는 코드입니다. 학습기를 돌리기 
> 직전헤 사용해주세요. (yolov5의 경우 파일 수가 대응되지 않는 경우는 해결해주지만, class_num이 초과되는 경때우는 에러를 발생시키기 때문)
> ### total_model.py
> 위 4 과정을 하나로 합친코드이지만, json파일 가공과정에서 사람의 실수에 의해 여러가지 에러가 발생할 수 있기 때문에 사용을 추천하지 않습니다.
> ### scanner.py
> 가장 큰 class_num와 지정한 class_num보다 더 큰 수를 가진 라벨링 파일들을 출력합니다.
> ### car_people_~.py
> 라벨링 대상을 바꾼 프로그램입니다. 코드 수정에 있어 참고해주세요.
> # Validation_maker (val_make.py)
> 주어진 데이터 셋 내에서 주어진 비율에 근접하게끔 무작위로 이미지/라벨을 추출해 validation dataset을 생성합니다.    
> 확률에 기반하기 때문에 100% 정확하지는 않지만, 데이터셋의 크기가 클 수록 주어진 목표치에 근사합니다.
> 만약, 데이터셋의 크기가 작은경우 다른방법을 사용해주세요.