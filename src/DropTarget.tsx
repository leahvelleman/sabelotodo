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
    depth?: number,
}

export const DroptargetTestId = 'droptarget'


const Droptarget: React.FunctionComponent<DroptargetProps> = ({dispatch, itemId=undefined, depth=0}) => {
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
            "Drop-target--dragging": canDrop,
            [`Drop-target--depth-${depth}`]: true,
        })}
         > 
            <div className={classSet({
                "Drop-target__line": true,
                "Drop-target__line--hover": isOver,
                "Drop-target__line--dragging": canDrop
            })}></div>
         </div>
    );
}

export default Droptarget;