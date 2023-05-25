from src import data
from src import plotting

jf1 = "GrabbingPrimitives/recordings/rec_5/processedAABBs.json"
jf2 = "GrabbingPrimitives/recordings/rec_6/processedAABBs.json"
jf3 = "GrabbingPrimitives/recordings/rec_7/processedAABBs.json"
jf4 = "GrabbingPrimitives/recordings/rec_8/processedAABBs.json"


def main():
    rec_data1 = data.RecordedData(jf1)
    
    hand_data = rec_data1.recorded_hands

    plotting.hand_data(hand_data)

    


























if __name__ == "__main__":
    main()