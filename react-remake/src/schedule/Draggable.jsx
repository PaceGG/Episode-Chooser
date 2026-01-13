/*
  React Drag & Drop components (single-file demo)
  - DraggableItem: wraps any content and makes it draggable
  - DroppableContainer: accepts draggables, supports reorder within list and transfer between lists
  - Uses HTML5 Drag and Drop API (with a simple keyboard mode)
  - Styling via styled-components

  Notes:
  - Install: npm install styled-components
  - This file exports default component DragAndDropDemo which demonstrates usage.

  This is JavaScript (not TypeScript) and uses React hooks.
*/

import React, { useState, useRef, useEffect } from "react";
import styled from "styled-components";

/* ================= Styled components ================= */
const ContainerRow = styled.div`
  display: flex;
  gap: 16px;
  padding: 16px;
  align-items: flex-start;
`;

const Column = styled.div`
  width: 320px;
  min-height: 120px;
  background: #f6f7fb;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 6px 18px rgba(16, 24, 40, 0.06);
`;

const Title = styled.h3`
  margin: 0 0 8px 0;
  font-size: 14px;
`;

const List = styled.div`
  background: transparent;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const ItemBox = styled.div`
  user-select: none;
  padding: 10px 12px;
  border-radius: 6px;
  background: white;
  box-shadow: 0 1px 0 rgba(16, 24, 40, 0.04);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: grab;
  transition: transform 160ms ease, box-shadow 160ms ease;
  &[aria-grabbed="true"] {
    opacity: 0.6;
    cursor: grabbing;
    transform: scale(0.98);
    box-shadow: 0 8px 20px rgba(16, 24, 40, 0.12);
  }
`;

const DropHighlight = styled.div`
  position: relative;
  &::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 8px;
    pointer-events: none;
    box-shadow: inset 0 0 0 3px rgba(99, 102, 241, 0.08);
  }
`;

const InsertIndicator = styled.div`
  height: 2px;
  background: rgba(99, 102, 241, 0.9);
  margin: 2px 0;
  border-radius: 2px;
  transition: opacity 120ms ease;
`;

const LiveRegion = styled.div`
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  overflow: hidden;
  white-space: nowrap;
`;

/* get insertion index within list based on mouse position and children bounding boxes */
function getIndexFromPosition(containerEl, clientY) {
  const children = Array.from(containerEl.children).filter(
    (c) => c.dataset && c.dataset.dnd !== "placeholder"
  );
  if (!children.length) return 0;
  for (let i = 0; i < children.length; i++) {
    const rect = children[i].getBoundingClientRect();
    const mid = rect.top + rect.height / 2;
    if (clientY < mid) return i;
  }
  return children.length; // append
}

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
  /* We expose both mouse drag (HTML5) and keyboard dragging via aria */
  const ref = useRef(null);

  const handleDragStart = (e) => {
    if (disabled) {
      e.preventDefault();
      return;
    }
    // set plain text payload so other browsers can read
    try {
      e.dataTransfer.setData("application/json", JSON.stringify({ id, type }));
    } catch (err) {
      e.dataTransfer.setData("text/plain", id);
    }
    e.dataTransfer.effectAllowed = "move"; // or copy/link based on props if extended
    if (onDragStart) onDragStart({ id, data, type });
    // small visual trick: setDragImage to a cloned node gives better preview
    const node = ref.current;
    if (node) {
      const clone = node.cloneNode(true);
      clone.style.boxShadow = "0 8px 20px rgba(16,24,40,0.12)";
      clone.style.padding = "10px 12px";
      clone.style.background = "white";
      clone.style.borderRadius = "6px";
      document.body.appendChild(clone);
      e.dataTransfer.setDragImage(
        clone,
        clone.offsetWidth / 2,
        clone.offsetHeight / 2
      );
      // remove clone after a tick
      setTimeout(() => document.body.removeChild(clone), 0);
    }
  };

  const handleDragEndLocal = () => {
    if (onDragEnd) onDragEnd({ id, data, type });
  };

  // Keyboard: pressing Space/Enter will "pick up" the item - this requires container to manage.
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
      <div style={{ flex: 1 }}>{children}</div>
      <div aria-hidden style={{ marginLeft: 10, opacity: 0.6 }}>
        ≡
      </div>
    </ItemBox>
  );
}

/* ================= DroppableContainer ================= */
function DroppableContainer({
  id,
  items = [],
  children,
  acceptTypes = ["item"],
  onReorder,
  onDrop,
  onDragStart,
  onDragEnd,
  placeholder = "Drop items here",
}) {
  const containerRef = useRef(null);
  const [internalItems, setInternalItems] = useState(items);
  const [dragging, setDragging] = useState(null); // {id, type, sourceId}
  const [over, setOver] = useState(false);
  const [insertIndex, setInsertIndex] = useState(null);
  const liveRef = useRef(null);

  useEffect(() => setInternalItems(items), [items]);

  useEffect(() => {
    if (insertIndex === null) return;
    // announce for screen reader
    if (liveRef.current) {
      liveRef.current.textContent = `Insert position ${insertIndex + 1} of ${
        internalItems.length + (dragging ? 1 : 0)
      }`;
    }
  }, [insertIndex, internalItems.length, dragging]);

  const handleDragEnter = (e) => {
    e.preventDefault();
    setOver(true);
  };

  const handleDragOver = (e) => {
    e.preventDefault(); // allow drop
    const dt = e.dataTransfer;
    // compute index
    const idx = getIndexFromPosition(containerRef.current, e.clientY);
    setInsertIndex(idx);
    // set correct dropEffect
    if (dt) dt.dropEffect = "move";
  };

  const handleDragLeave = (e) => {
    // if leaving to child, ignore
    const current = containerRef.current;
    if (!current) return setOver(false);
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
    const droppedId = payload && payload.id;
    const droppedType = payload && payload.type;
    if (!droppedId) return;
    if (!acceptTypes.includes(droppedType)) return; // ignoring incompatible type

    // If item is already inside same container, reorder
    const existingIndex = internalItems.findIndex((it) => it.id === droppedId);

    // If reorder within same list
    if (existingIndex !== -1) {
      const newIndex =
        insertIndex === null ? internalItems.length : insertIndex;
      if (newIndex !== existingIndex && newIndex !== existingIndex + 1) {
        const arr = [...internalItems];
        const [removed] = arr.splice(existingIndex, 1);
        const insertAt = newIndex > existingIndex ? newIndex - 1 : newIndex;
        arr.splice(insertAt, 0, removed);
        setInternalItems(arr);
        if (onReorder) onReorder(arr);
      }
    } else {
      // item from another list: in a real app you would receive the full data object; here we emit onDrop so parent can handle
      const newIndex =
        insertIndex === null ? internalItems.length : insertIndex;
      const arr = [...internalItems];
      // ask parent to provide item data by calling onDrop
      if (onDrop) {
        const provided = onDrop({
          id: droppedId,
          type: droppedType,
          targetId: id,
          index: newIndex,
        });
        // if onDrop returns a data object synchronously we insert it
        if (provided && provided.id) {
          arr.splice(newIndex, 0, provided);
          setInternalItems(arr);
          if (onReorder) onReorder(arr);
        }
      }
    }
    setInsertIndex(null);
  };

  const handleDragStartLocal = (info) => {
    setDragging(info);
    if (onDragStart) onDragStart(info);
  };

  const handleDragEndLocal = (info) => {
    setDragging(null);
    setInsertIndex(null);
    if (onDragEnd) onDragEnd(info);
  };

  const renderedChildren =
    children ||
    internalItems.map((it) => (
      <DraggableItem
        key={it.id}
        id={it.id}
        data={it}
        type={it.type || "item"}
        onDragStart={handleDragStartLocal}
        onDragEnd={handleDragEndLocal}
      >
        {it.content}
      </DraggableItem>
    ));

  // render list of children with an insert indicator
  const childElements = React.Children.toArray(renderedChildren).map(
    (child, idx) => {
      // we wrap each child to be able to detect bounding box etc.
      const showBefore = insertIndex === idx && over;
      return (
        <div key={child.key} data-dnd="wrapper">
          {showBefore && <InsertIndicator />}
          {child}
        </div>
      );
    }
  );

  // if insertIndex === internalItems.length
  const appendIndicator =
    insertIndex === internalItems.length && over ? <InsertIndicator /> : null;

  return (
    <Column>
      <Title>List — {id}</Title>
      <DropHighlight>
        <List
          ref={containerRef}
          role="list"
          aria-label={`Droppable list ${id}`}
          onDragEnter={handleDragEnter}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          tabIndex={0}
          style={over ? { outline: "2px solid rgba(99,102,241,0.12)" } : {}}
          data-dnd="container"
        >
          {internalItems.length === 0 ? (
            <div data-dnd="placeholder">{placeholder}</div>
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

/* ================= Demo usage (default export) ================= */
export default function DragAndDropDemo() {
  const initialA = [
    { id: "a1", content: "Card A1" },
    { id: "a2", content: "Card A2" },
    { id: "a3", content: "Card A3" },
  ];
  const initialB = [
    { id: "b1", content: "Card B1" },
    { id: "b2", content: "Card B2" },
  ];

  const [listA, setListA] = useState(initialA);
  const [listB, setListB] = useState(initialB);

  // top-level handlers
  const handleDrop = ({ id, type, targetId, index }) => {
    let moved = null;
    if (listA.find((x) => x.id === id)) {
      moved = listA.find((x) => x.id === id);
      setListA((s) => s.filter((x) => x.id !== id));
    }
    if (!moved && listB.find((x) => x.id === id)) {
      moved = listB.find((x) => x.id === id);
      setListB((s) => s.filter((x) => x.id !== id));
    }
    if (!moved) return null;
    // insert into target list state synchronously
    if (targetId === "list-1") {
      setListA((prev) => {
        const copy = [...prev];
        copy.splice(index, 0, moved);
        return copy;
      });
      return moved;
    } else if (targetId === "list-2") {
      setListB((prev) => {
        const copy = [...prev];
        copy.splice(index, 0, moved);
        return copy;
      });
      return moved;
    }
    return null;
  };

  const handleReorderA = (newOrder) => setListA(newOrder);
  const handleReorderB = (newOrder) => setListB(newOrder);

  const onDragStart = (info) => console.log("drag start", info);
  const onDragEnd = (info) => console.log("drag end", info);

  return (
    <div>
      <ContainerRow>
        <DroppableContainer
          id="list-1"
          items={listA}
          acceptTypes={["item"]}
          onDrop={handleDrop}
          onReorder={handleReorderA}
          onDragStart={onDragStart}
          onDragEnd={onDragEnd}
          persistence={false}
        />
        <DroppableContainer
          id="list-2"
          items={listB}
          acceptTypes={["item"]}
          onDrop={handleDrop}
          onReorder={handleReorderB}
          onDragStart={onDragStart}
          onDragEnd={onDragEnd}
          persistence={false}
        />
      </ContainerRow>
    </div>
  );
}
