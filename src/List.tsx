import React, { useState } from 'react';
import classSet from 'react-classset';
import {useDrag, DragObjectWithType} from 'react-dnd';
import './List.scss';
import {ListItem, Action} from './interfaces'
import {DragItemTypes} from './Constants'
import DropTarget from './DropTarget';


interface ListProps {
    myList: ListItem,
    isChild: boolean,
    dispatch: (arg0:Action) => void,
    depth?: number,
}

export interface DragListItemWithType extends DragObjectWithType {
    id: number,
    parentId: number,
}


const List: React.FunctionComponent<ListProps> = ({myList, isChild, dispatch, depth=0}) => {
    const [expanded, setExpanded] = useState(false);
    const [{ isDragging }, drag, preview] = useDrag({
        item: { 
            type: DragItemTypes.LIST,
            id: myList.id ,
            parentId: myList.parent,
        } as DragListItemWithType,
        collect: monitor => ({
          isDragging: !!monitor.isDragging(),
        }),
      })
    const depthClass = `List--depth-${depth}`;
    return (
        <React.Fragment>
        <div 
            className={classSet({
                'List': true,
                'List--child': isChild,
                'List--dragging': isDragging,
                [depthClass]: true
            })} 
            ref={preview}
            key={myList.id}   
        >
            <div className="List-dnd-target" ref={drag}></div>
            <div className="List-content">
                <header className="List-header">
                 <h1>
                    <span 
                        className="List__expand-arrow" 
                        onClick={() => setExpanded(!expanded)}
                        data-testid="list-expanded"
                    >
                        {myList.children && (expanded? '⯆' : '⯈')}
                    </span> 
                    {myList.name}
                </h1>
                </header>
                <main>
                </main>
  
            </div>
            
        </div>
        <DropTarget dispatch={dispatch} itemId={myList.id} depth={depth}/>
        {myList.children && expanded && myList.children.map((sublist: ListItem) => {
                            return <List 
                                        myList={sublist} 
                                        isChild={true} 
                                        key={sublist.id} 
                                        dispatch={dispatch}
                                        depth={depth+1}
                                    />
        })}
        </React.Fragment>
    );
}

export default List;
