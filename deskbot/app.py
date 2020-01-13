from deskbot import constant as cs, controller as ctr, processor as ps
import time


def test_match(controller):
    controller.screen_shot()
    top_left, bottom_right = ps.match_all(threshold=0.15)
    print(f'Top Left: {top_left}, Bottom Right: {bottom_right}')
    if top_left != -1:
        print('Clicking on valid locations')
        controller.click_within(top_left, bottom_right)


def test_diff(controller, processor):
    controller.screen_shot()
    time.sleep(0.5)
    processor.check_difference()


def run():
    controller = ctr.Controller(cs.DUEL_LINKS)
    processor = ps.Processor(controller)
    test_diff(controller, processor)
    # test_match(controller)







