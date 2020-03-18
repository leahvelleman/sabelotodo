import {Item, Action} from './interfaces'
import { MOVE_ITEM } from './itemActions'

type ItemState = {
    items: Item[]
}

const itemReducer = (state:ItemState, action:Action): ItemState => {
    switch (action.type) {
        case MOVE_ITEM:
            return ({
                ...state,
                items: state.items.map((item:Item) => {
                    if(item.id === action.draggedId) {
                        return {...item, parent: action.droppedId}
                    }
                    return item;
                }),
            })
        default:
            return state;
    }
}

export default itemReducer;
