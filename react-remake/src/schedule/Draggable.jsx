/*   React Drag & Drop components (single-file demo)   - DraggableItem: wraps any content and makes it draggable   - DroppableContainer: accepts draggables, supports reorder within list and transfer between lists   - Uses HTML5 Drag and Drop API (with a simple keyboard mode)   - Uses MUI Chip components for demo    Notes:   - Install: npm install styled-components @mui/material @mui/icons-material @emotion/react @emotion/styled   - This file exports default component DragAndDropDemo which demonstrates usage.*/
import React, { useState, useRef, useEffect } from "react";
import styled from "styled-components";
import Chip from "@mui/material/Chip";
import DragIndicatorIcon from "@mui/icons-material/DragIndicator";
import { Box } from "@mui/material";

const ContainerRow = styled.div`
  display: flex;
  gap: 24px;
  padding: 24px;
  align-items: flex-start;
  background: #f8fafc;
  min-height: 100vh;
`;

const Column = styled.div`
  width: 350px;
  min-height: 200px;
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
`;

const Title = styled.h3`
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const List = styled.div`
  background: transparent;
  min-height: 120px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 4px;
`;

const ItemBox = styled.div`
  user-select: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: grab;
  transition: all 0.2s ease;

  &:hover {
    border-color: #94a3b8;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  }

  &[aria-grabbed="true"] {
    opacity: 0.7;
    cursor: grabbing;
    transform: scale(0.99) rotate(1deg);
    border-color: #6366f1;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
    background: #f8fafc;
  }

  &.dragging-over {
    border-color: #6366f1;
    background: #f0f9ff;
  }
`;

const DropHighlight = styled.div`
  position: relative;
  &::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 12px;
    pointer-events: none;
    box-shadow: inset 0 0 0 2px rgba(99, 102, 241, 0.3);
    opacity: 0;
    transition: opacity 0.2s ease;
  }

  &.over::after {
    opacity: 1;
  }
`;

const InsertIndicator = styled.div`
  height: 3px;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  margin: 4px 8px;
  border-radius: 3px;
  opacity: 0;
  transform: scaleY(0);
  transition: all 0.2s ease;

  &.visible {
    opacity: 1;
    transform: scaleY(1);
  }
`;

const LiveRegion = styled.div`
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  overflow: hidden;
  white-space: nowrap;
`;

const Placeholder = styled.div`
  text-align: center;
  padding: 32px 16px;
  color: #94a3b8;
  font-size: 14px;
  background: #f8fafc;
  border-radius: 8px;
  border: 2px dashed #cbd5e1;
  margin: 4px;
`;

const DragHandle = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  color: #94a3b8;
  cursor: grab;
  border-radius: 4px;

  &:hover {
    background: #f1f5f9;
    color: #64748b;
  }

  & > svg {
    width: 18px;
    height: 18px;
  }
`;

/* ================= DraggableItem ================= */
function DraggableItem({
  id,
  data,
  type = "item",
  disabled = false,
  onDragStart,
  onDragEnd,
  children,
}) {
  const ref = useRef(null);

  const handleDragStart = (e) => {
    if (disabled) {
      e.preventDefault();
      return;
    }

    try {
      e.dataTransfer.setData("application/json", JSON.stringify({ id, type }));
    } catch (err) {
      e.dataTransfer.setData("text/plain", id);
    }

    e.dataTransfer.effectAllowed = "move";
    if (onDragStart) onDragStart({ id, data, type });

    const node = ref.current;
    if (node) {
      const clone = node.cloneNode(true);
      clone.style.boxShadow = "0 12px 32px rgba(0, 0, 0, 0.15)";
      clone.style.padding = "12px";
      clone.style.background = "white";
      clone.style.borderRadius = "8px";
      clone.style.width = `${node.offsetWidth}px`;
      clone.style.opacity = "0.9";
      document.body.appendChild(clone);
      e.dataTransfer.setDragImage(
        clone,
        clone.offsetWidth / 2,
        clone.offsetHeight / 2
      );
      setTimeout(() => document.body.removeChild(clone), 0);
    }
  };

  const handleDragEndLocal = () => {
    if (onDragEnd) onDragEnd({ id, data, type });
  };

  return (
    <ItemBox
      ref={ref}
      role="listitem"
      aria-grabbed={false}
      draggable={!disabled}
      tabIndex={disabled ? -1 : 0}
      data-id={id}
      data-type={type}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEndLocal}
      data-dnd="item"
    >
      <div
        style={{ flex: 1, display: "flex", alignItems: "center", gap: "12px" }}
      >
        <DragHandle>
          <DragIndicatorIcon />
        </DragHandle>
        <div style={{ flex: 1 }}>{children}</div>
      </div>
    </ItemBox>
  );
}

/* ================= DroppableContainer ================= */
function DroppableContainer({
  id,
  children = [], // теперь принимаем массив компонентов
  acceptTypes = ["item"],
  onReorder,
  onDrop,
  onDragStart,
  onDragEnd,
  placeholder = "Drop items here",
  title,
}) {
  const containerRef = useRef(null);
  const [internalChildren, setInternalChildren] = useState(children);
  const [over, setOver] = useState(false);
  const [insertIndex, setInsertIndex] = useState(null);
  const liveRef = useRef(null);

  useEffect(() => setInternalChildren(children), [children]);

  const getIndexFromPosition = (clientY) => {
    const containerEl = containerRef.current;
    const children = Array.from(containerEl.children).filter(
      (c) => c.dataset && c.dataset.dnd !== "placeholder"
    );
    if (!children.length) return 0;

    for (let i = 0; i < children.length; i++) {
      const rect = children[i].getBoundingClientRect();
      const mid = rect.top + rect.height / 2;
      if (clientY < mid) return i;
    }
    return children.length;
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    setOver(true);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    const dt = e.dataTransfer;
    const idx = getIndexFromPosition(e.clientY);
    setInsertIndex(idx);
    if (dt) dt.dropEffect = "move";
  };

  const handleDragLeave = (e) => {
    const current = containerRef.current;
    if (!current) {
      setOver(false);
      return;
    }

    const rect = current.getBoundingClientRect();
    if (
      e.clientX < rect.left ||
      e.clientX > rect.right ||
      e.clientY < rect.top ||
      e.clientY > rect.bottom
    ) {
      setOver(false);
      setInsertIndex(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setOver(false);

    let payload = null;
    try {
      payload = JSON.parse(e.dataTransfer.getData("application/json"));
    } catch (err) {
      payload = { id: e.dataTransfer.getData("text/plain") };
    }

    const droppedId = payload?.id;
    const droppedType = payload?.type;

    if (!droppedId || !acceptTypes.includes(droppedType)) {
      setInsertIndex(null);
      return;
    }

    // Получаем индекс элемента среди draggable детей
    const childArray = React.Children.toArray(internalChildren);
    const existingIndex = childArray.findIndex(
      (child) => child.props && child.props.id === droppedId
    );

    const newIndex = insertIndex === null ? childArray.length : insertIndex;

    if (existingIndex !== -1) {
      // Reorder within same container
      if (newIndex !== existingIndex && newIndex !== existingIndex + 1) {
        const newChildren = [...childArray];
        const [removed] = newChildren.splice(existingIndex, 1);
        const insertAt = newIndex > existingIndex ? newIndex - 1 : newIndex;
        newChildren.splice(insertAt, 0, removed);
        setInternalChildren(newChildren);
        if (onReorder) onReorder(newChildren);
      }
    } else {
      // Item from another container
      if (onDrop) {
        const provided = onDrop({
          id: droppedId,
          type: droppedType,
          targetId: id,
          index: newIndex,
        });

        if (provided) {
          const newChildren = [...childArray];
          newChildren.splice(newIndex, 0, provided);
          setInternalChildren(newChildren);
          if (onReorder) onReorder(newChildren);
        }
      }
    }

    setInsertIndex(null);
  };

  const handleDragStartLocal = (info) => {
    if (onDragStart) onDragStart(info);
  };

  const handleDragEndLocal = (info) => {
    setInsertIndex(null);
    if (onDragEnd) onDragEnd(info);
  };

  const renderedChildren = React.Children.map(internalChildren, (child) => {
    if (child && child.props && child.props.id) {
      return (
        <DraggableItem
          key={child.props.id}
          id={child.props.id}
          data={child.props.data}
          type={child.props.type || "item"}
          onDragStart={handleDragStartLocal}
          onDragEnd={handleDragEndLocal}
        >
          {child}
        </DraggableItem>
      );
    }
    return child;
  });

  const childElements = React.Children.toArray(renderedChildren).map(
    (child, idx) => {
      const showBefore = insertIndex === idx && over;
      return (
        <div key={child.key || idx} data-dnd="wrapper">
          {showBefore && <InsertIndicator className="visible" />}
          {child}
        </div>
      );
    }
  );

  const appendIndicator =
    insertIndex === React.Children.count(internalChildren) && over ? (
      <InsertIndicator className="visible" />
    ) : null;

  return (
    <Column>
      {title && <Title>{title}</Title>}
      <DropHighlight className={over ? "over" : ""}>
        <List
          ref={containerRef}
          role="list"
          aria-label={`Droppable list ${id}`}
          onDragEnter={handleDragEnter}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          tabIndex={0}
          style={over ? { backgroundColor: "rgba(99, 102, 241, 0.02)" } : {}}
          data-dnd="container"
        >
          {React.Children.count(internalChildren) === 0 ? (
            <Placeholder data-dnd="placeholder">{placeholder}</Placeholder>
          ) : (
            <>
              {childElements}
              {appendIndicator}
            </>
          )}
        </List>
      </DropHighlight>
      <LiveRegion aria-live="polite" ref={liveRef} />
    </Column>
  );
}

function Draggable({ children }) {
  const childArray = React.Children.toArray(children).filter(Boolean);

  const [containers, setContainers] = useState(() => {
    const map = {};
    childArray.forEach((child, idx) => {
      const cid = child?.props?.id || `col-${idx}`;
      const childElems = React.Children.toArray(child?.props?.children || []);
      map[cid] = childElems.map((el, j) => {
        const id = el?.props?.id || `${cid}-item-${j}`;
        return { id, element: el };
      });
    });
    return map;
  });

  // Найти и удалить элемент из текущего состояния, вернуть найденный и новый map
  const findAndRemove = (id) => {
    let found = null;
    const newMap = {};
    Object.entries(containers).forEach(([cid, items]) => {
      const idx = items.findIndex((it) => it.id === id);
      if (idx !== -1) {
        found = items[idx];
        newMap[cid] = [...items.slice(0, idx), ...items.slice(idx + 1)];
      } else {
        newMap[cid] = items;
      }
    });
    return [found, newMap];
  };

  const handleDrop = ({ id, type, targetId, index }) => {
    // Удаляем из предыдущего контейнера и вставляем в target
    const [found, without] = findAndRemove(id);
    if (!found) return null;

    const targetItems = [...(without[targetId] || [])];
    const insertAt = Math.max(0, Math.min(index, targetItems.length));
    targetItems.splice(insertAt, 0, found);
    const newMap = { ...without, [targetId]: targetItems };
    setContainers(newMap);

    // Возвращаем React элемент с корректным props.id — DroppableContainer вставит его
    return React.cloneElement(found.element, {
      id: found.id,
      data: found.data,
      type: "item",
    });
  };

  const handleReorder = (containerId) => (newChildren) => {
    const ids = newChildren
      .map((ch) => ch.props && ch.props.id)
      .filter(Boolean);
    setContainers((prev) => {
      const items = prev[containerId] || [];
      const lookup = items.reduce((acc, it) => {
        acc[it.id] = it;
        return acc;
      }, {});
      return {
        ...prev,
        [containerId]: ids.map(
          (id) => lookup[id] || { id, element: <div id={id}>{id}</div> }
        ),
      };
    });
  };

  return (
    <ContainerRow>
      {childArray.map((child, idx) => {
        const cid = child?.props?.id || `col-${idx}`;
        const title = child?.props?.title || `List ${idx + 1}`;
        const items = containers[cid] || [];
        const childrenForContainer = items.map((it) =>
          React.cloneElement(it.element, { id: it.id, key: it.id })
        );

        return (
          <DroppableContainer
            key={cid}
            id={cid}
            title={title}
            onDrop={handleDrop}
            onReorder={handleReorder(cid)}
          >
            {childrenForContainer}
          </DroppableContainer>
        );
      })}
    </ContainerRow>
  );
}

// Пример использования: просто пишем несколько <DroppableContainer> внутри <Draggable>
export default function DragAndDropDemo() {
  return (
    <Draggable>
      <DroppableContainer title="To do">
        <Box sx={{ bgcolor: "red" }}>Box item</Box>
        <Chip label="Fix bug #42" />
      </DroppableContainer>

      <DroppableContainer title="In progress">
        <Chip label="Loading UI" />
      </DroppableContainer>

      <DroppableContainer title="Done">
        <Chip label="Ship v1.0" />
      </DroppableContainer>
    </Draggable>
  );
}
