import {Action} from './interfaces';

export const MOVE_ITEM = 'MOVE_ITEM';
export const moveItemAction = (draggedId:number, droppedId: number | undefined): Action => {
    return {
        type: MOVE_ITEM,
        draggedId: draggedId,
        droppedId: droppedId,
    }
}