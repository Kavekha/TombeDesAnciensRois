import libtcodpy as libtcod

from game_messages import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full.', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up {} {}!'.format(str(item.item.stack), item.name), libtcod.blue)
            })

            # v15 stack item.
            for i in self.items:
                print('DEBUG : item is {}, compared to {}', i, item)
                # v15 : meme fonction, ignore les stats differentes et autres criteres uniques (plus tard).
                if i.item.use_function == item.item.use_function:
                    print('DEBUG : item found, stack created!')
                    i.item.stack += 1
                    break
            else:
                print('DEBUG : item not found, added.')
                self.items.append(item)

        return results

    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('The {} cannot be used.'.format(item_entity.name), libtcod.yellow)})
        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item, nb_to_remove=1):
        # v15 : stack
        if nb_to_remove > item.item.stack:
            nb_to_remove = item.item.stack

        if item.item.stack > nb_to_remove:
            item.item.stack -= nb_to_remove
        else:
            self.items.remove(item)

    def drop_item(self, item):
        results = []

        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)

        # v15 : stack. Dirty. If dropped with 2 stacks, the item will be on the floor AND in inventory.
        # Dropping the second stack will teleport the one already dropped.
        # for now, all the stack are dropped.

        item.x = self.owner.x
        item.y = self.owner.y

        # v15 stack system
        if item.item.stack > 1:
            results.append({'item_dropped': item, 'message': Message('You dropped {} {}'.format(str(item.item.stack), item.name), libtcod.yellow)})
        else:
            results.append({'item_dropped': item, 'message': Message('You dropped the {}'.format(item.name), libtcod.yellow)})

        # v15 : all to drop the full stack.
        self.remove_item(item, nb_to_remove=999)

        return results
