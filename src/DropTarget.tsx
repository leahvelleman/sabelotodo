import React from 'react';
import classSet from 'react-classset';
import {useDrop} from 'react-dnd';
import {DragItemTypes} from './Constants'
import { moveItemAction, setExpandedAction } from './itemActions';
import './DropTarget.scss';
import { Action } from './interfaces';
import {DragListItemWithType} from './List'


interface DroptargetProps {
    dispatch: (arg0:Action) => void,
    itemId?: number | undefined,
    depth?: number,
    parentIds: number[],
    setExpanded?(arg0: boolean): void,
}

export const DroptargetTestId = 'droptarget'


const Droptarget: React.FunctionComponent<DroptargetProps> = ({dispatch, itemId=undefined, depth=0, parentIds, setExpanded}) => {
    const [{isOver, canDrop}, drop] = useDrop({
        accept: DragItemTypes.LIST,
        //@ts-ignore
        drop: (target):void => {
            dispatch(moveItemAction(target.id, itemId))
            if(itemId) {
                dispatch(setExpandedAction(itemId, true))
            }
        },
        canDrop: (target:DragListItemWithType):boolean => {
            const isOwnParent = parentIds.includes(target.id)
            return target.id !== itemId && target.parentId !== itemId && !isOwnParent
        },
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
            "Drop-target--hover": canDrop && isOver,
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