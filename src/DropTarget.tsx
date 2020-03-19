import React from 'react';
import classSet from 'react-classset';
import {useDrop} from 'react-dnd';
import {DragItemTypes} from './Constants'
import { moveItemAction } from './itemActions';
import './DropTarget.scss';
import { Action } from './interfaces';
import {DragListItemWithType} from './List'

interface DroptargetProps {
    dispatch: (arg0:Action) => void,
    itemId?: number | undefined,
}

export const DroptargetTestId = 'droptarget'


const Droptarget: React.FunctionComponent<DroptargetProps> = ({dispatch, itemId=undefined}) => {
    const [{isOver, canDrop}, drop] = useDrop({
        accept: DragItemTypes.LIST,
        //@ts-ignore
        drop: (target):void => dispatch(moveItemAction(target.id, itemId)),
        
        canDrop: (target:DragListItemWithType):boolean => target.id !== itemId && target.parentId !== itemId,
        collect: monitor => ({
            isOver: !!monitor.isOver(),
            canDrop: monitor.canDrop(),
		}),
    })
    return (
        <div 
            ref={drop}
            data-testid={DroptargetTestId}
            className={classSet({
            "Drop-target": true,
            "Drop-target--hover": isOver,
            "Drop-target--dragging": canDrop
        })}
         > </div>
    );
}

export default Droptarget;