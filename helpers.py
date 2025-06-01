# helpers.py

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List

@allure.step("Drag and drop элемента {source} на {target}")
def drag_and_drop(driver: WebDriver, source: WebElement, target: WebElement) -> None:
    driver.execute_script("""
    function simulateDragDrop(sourceNode, destinationNode) {
        const EVENT_TYPES = {
            DRAG_START: 'dragstart',
            DRAG_OVER: 'dragover',
            DROP: 'drop'
        };
        function createEvent(type) {
            const event = new DragEvent(type, {
                bubbles: true,
                cancelable: true,
                dataTransfer: new DataTransfer()
            });
            return event;
        }
        sourceNode.dispatchEvent(createEvent(EVENT_TYPES.DRAG_START));
        destinationNode.dispatchEvent(createEvent(EVENT_TYPES.DRAG_OVER));
        destinationNode.dispatchEvent(createEvent(EVENT_TYPES.DROP));
    }
    simulateDragDrop(arguments[0], arguments[1]);
    """, source, target)

@allure.step("Проверить наличие заказа {order_number} в списке")
def is_order_in_list(order_numbers: List[str], order_number: str) -> bool:
    return str(order_number) in order_numbers